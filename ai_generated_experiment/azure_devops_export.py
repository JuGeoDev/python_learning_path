#!/usr/bin/env python3
"""
Azure DevOps export helper.

What it does:
- Runs a WIQL query to collect work item IDs
- Fetches work items in batches of up to 200 IDs
- Saves each work item as JSON and Markdown
- Downloads attachments found in work item relations
- Optionally clones a wiki Git repository for Markdown-based wiki export

Requirements:
- Python 3.10+
- No third-party Python packages required
- Optional: git installed, if you use --wiki-clone-url

Usage example:
  export AZDO_PAT="..."
  python azure_devops_export.py \
    --org myorg \
    --project MyProject \
    --out ./azdo_export \
    --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project ORDER BY [System.ChangedDate] DESC" \
    --fields System.Id System.Title System.State System.AssignedTo System.Tags System.CreatedDate System.ChangedDate

Notes:
- Azure DevOps REST requests should include api-version=7.1.
- WIQL returns IDs; work item details are fetched separately.
- Work items batch endpoints accept a maximum of 200 IDs per request.
- Attachments are downloaded separately from their attachment URL.
"""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlencode, urlparse
from urllib.request import Request, urlopen


API_VERSION = "7.1"
MAX_BATCH = 200


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def slugify(text: str, fallback: str = "item") -> str:
    text = text or ""
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text[:120] or fallback


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def basic_auth_header(pat: str) -> str:
    token = base64.b64encode(f":{pat}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def request_json(method: str, url: str, pat: str, body: dict | None = None) -> dict:
    data = None
    headers = {
        "Authorization": basic_auth_header(pat),
        "Accept": "application/json",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = Request(url=url, method=method.upper(), headers=headers, data=data)
    with urlopen(req, timeout=120) as resp:
        raw = resp.read()
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))


def request_bytes(url: str, pat: str) -> bytes:
    headers = {
        "Authorization": basic_auth_header(pat),
        "Accept": "*/*",
    }
    req = Request(url=url, method="GET", headers=headers)
    with urlopen(req, timeout=120) as resp:
        return resp.read()


def chunked(seq: Sequence[int], size: int) -> Iterable[list[int]]:
    for i in range(0, len(seq), size):
        yield list(seq[i:i + size])


def normalize_datetime(value: str | None) -> str:
    if not value:
        return ""
    return value.replace("T", " ").replace("Z", " UTC")


def extract_fields(work_item: dict) -> dict:
    return work_item.get("fields", {}) or {}


def relation_target_url(rel: dict) -> str:
    return rel.get("url", "")


def relation_type(rel: dict) -> str:
    return rel.get("rel", "")


def attachment_file_name_from_content_url(content_url: str, default: str) -> str:
    parsed = urlparse(content_url)
    name = Path(parsed.path).name
    if name:
        return name
    return default


def download_attachment(
    pat: str,
    attachment_url: str,
    output_dir: Path,
    work_item_id: int,
    relation_index: int,
) -> str:
    ensure_dir(output_dir)
    default_name = f"wi-{work_item_id}-attachment-{relation_index}"
    filename = attachment_file_name_from_content_url(attachment_url, default_name)
    out_path = output_dir / filename
    if out_path.exists():
        return str(out_path)

    content = request_bytes(attachment_url, pat)
    out_path.write_bytes(content)
    return str(out_path)


def build_markdown(work_item: dict, attachment_paths: list[str]) -> str:
    fields = extract_fields(work_item)
    wid = work_item.get("id", "")
    title = fields.get("System.Title", "")
    state = fields.get("System.State", "")
    assigned_to = fields.get("System.AssignedTo", "")
    created = normalize_datetime(fields.get("System.CreatedDate"))
    changed = normalize_datetime(fields.get("System.ChangedDate"))
    area = fields.get("System.AreaPath", "")
    iteration = fields.get("System.IterationPath", "")
    tags = fields.get("System.Tags", "")
    description = fields.get("System.Description", "")

    lines = [
        f"# {title or f'Work Item {wid}'}",
        "",
        f"- ID: {wid}",
        f"- State: {state}",
        f"- Assigned To: {assigned_to}",
        f"- Area Path: {area}",
        f"- Iteration Path: {iteration}",
        f"- Created: {created}",
        f"- Changed: {changed}",
        f"- Tags: {tags}",
        "",
        "## Description",
        "",
        description or "_No description_",
    ]

    if attachment_paths:
        lines.extend([
            "",
            "## Attachments",
            "",
        ])
        for p in attachment_paths:
            rel = Path(p).name
            lines.append(f"- [{rel}](./attachments/{rel})")

    relations = work_item.get("relations", []) or []
    if relations:
        lines.extend([
            "",
            "## Relations",
            "",
        ])
        for rel in relations:
            rtype = relation_type(rel)
            url = relation_target_url(rel)
            lines.append(f"- {rtype}: {url}")

    return "\n".join(lines).strip() + "\n"


def export_work_items(
    org: str,
    project: str,
    pat: str,
    out_dir: Path,
    wiql: str,
    fields: list[str],
    expand: str,
    download_attachments: bool,
) -> None:
    api_base = f"https://dev.azure.com/{quote(org)}/{quote(project)}/_apis"
    wiql_url = f"{api_base}/wit/wiql?api-version={API_VERSION}"
    eprint(f"Running WIQL query against {wiql_url}")
    wiql_result = request_json("POST", wiql_url, pat, {"query": wiql})

    work_items = wiql_result.get("workItems", []) or []
    ids = [int(item["id"]) for item in work_items if "id" in item]
    eprint(f"Found {len(ids)} work item IDs")

    raw_dir = out_dir / "raw"
    md_dir = out_dir / "markdown"
    attach_dir = out_dir / "attachments"
    ensure_dir(raw_dir)
    ensure_dir(md_dir)
    ensure_dir(attach_dir)

    summary_rows = []

    for batch_no, id_batch in enumerate(chunked(ids, MAX_BATCH), start=1):
        batch_url = f"{api_base}/wit/workitemsbatch?api-version={API_VERSION}"
        eprint(f"Fetching batch {batch_no} ({len(id_batch)} items)")
        payload = {
            "ids": id_batch,
            "fields": fields,
            "$expand": expand,
        }
        batch_result = request_json("POST", batch_url, pat, payload)
        items = batch_result.get("value", batch_result if isinstance(batch_result, list) else [])  # be tolerant

        if isinstance(items, dict):
            items = [items]

        for item in items:
            item_id = int(item.get("id"))
            fields_obj = extract_fields(item)
            title = fields_obj.get("System.Title", f"Work Item {item_id}")
            item_slug = f"{item_id}-{slugify(title)}"

            item_raw_path = raw_dir / f"{item_slug}.json"
            item_raw_path.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")

            attachment_paths: list[str] = []
            if download_attachments:
                for rel_index, rel in enumerate(item.get("relations", []) or [], start=1):
                    if relation_type(rel) == "AttachedFile":
                        attachment_url = relation_target_url(rel)
                        try:
                            downloaded = download_attachment(
                                pat=pat,
                                attachment_url=attachment_url,
                                output_dir=attach_dir,
                                work_item_id=item_id,
                                relation_index=rel_index,
                            )
                            attachment_paths.append(downloaded)
                        except Exception as exc:
                            eprint(f"  ! attachment download failed for WI {item_id}: {exc}")

            md = build_markdown(item, attachment_paths)
            md_path = md_dir / f"{item_slug}.md"
            md_path.write_text(md, encoding="utf-8")

            summary_rows.append({
                "id": item_id,
                "title": title,
                "state": fields_obj.get("System.State", ""),
                "assigned_to": fields_obj.get("System.AssignedTo", ""),
                "markdown": str(md_path.relative_to(out_dir)),
                "raw": str(item_raw_path.relative_to(out_dir)),
            })

    summary_path = out_dir / "summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "state", "assigned_to", "markdown", "raw"])
        writer.writeheader()
        writer.writerows(summary_rows)

    eprint(f"Wrote summary: {summary_path}")


def clone_wiki_repo(clone_url: str, out_dir: Path) -> None:
    ensure_dir(out_dir)
    target = out_dir / "wiki"
    if target.exists() and any(target.iterdir()):
        eprint(f"Wiki folder already exists, skipping clone: {target}")
        return

    cmd = ["git", "clone", clone_url, str(target)]
    eprint("Cloning wiki repo:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def build_wiki_clone_url(org: str, project: str, wiki_repo_name: str) -> str:
    # Example patterns vary by wiki type; this is the standard Azure DevOps Git URL form.
    # Users can override it with --wiki-clone-url if their repo uses a different name.
    return f"https://dev.azure.com/{org}/{project}/_git/{wiki_repo_name}"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export Azure DevOps work items, attachments, and wiki markdown.")
    p.add_argument("--org", required=True, help="Azure DevOps organization name")
    p.add_argument("--project", required=True, help="Azure DevOps project name")
    p.add_argument("--pat", default=os.environ.get("AZDO_PAT", ""), help="Personal access token (or set AZDO_PAT)")
    p.add_argument("--out", default="./azdo_export", help="Output directory")
    p.add_argument(
        "--wiql",
        default="SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project ORDER BY [System.ChangedDate] DESC",
        help="WIQL query used to collect work item IDs",
    )
    p.add_argument(
        "--fields",
        nargs="+",
        default=[
            "System.Id",
            "System.Title",
            "System.State",
            "System.AssignedTo",
            "System.Tags",
            "System.AreaPath",
            "System.IterationPath",
            "System.CreatedDate",
            "System.ChangedDate",
            "System.Description",
        ],
        help="Work item fields to fetch",
    )
    p.add_argument(
        "--expand",
        default="Relations",
        choices=["None", "Relations", "Fields", "Links", "All"],
        help="Work item expansion mode",
    )
    p.add_argument(
        "--no-attachments",
        action="store_true",
        help="Do not download attached files",
    )
    p.add_argument(
        "--wiki-clone-url",
        default="",
        help="Optional wiki Git clone URL. If set, the script clones the wiki repo into <out>/wiki.",
    )
    p.add_argument(
        "--wiki-repo-name",
        default="",
        help="Optional wiki repo name used to build a default clone URL if --wiki-clone-url is not provided.",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if not args.pat:
        eprint("Missing PAT. Pass --pat or set AZDO_PAT.")
        return 2

    out_dir = Path(args.out).resolve()
    ensure_dir(out_dir)

    if args.wiki_clone_url:
        try:
            clone_wiki_repo(args.wiki_clone_url, out_dir)
        except subprocess.CalledProcessError as exc:
            eprint(f"Wiki clone failed: {exc}")
            return 1
    elif args.wiki_repo_name:
        try:
            clone_wiki_repo(build_wiki_clone_url(args.org, args.project, args.wiki_repo_name), out_dir)
        except subprocess.CalledProcessError as exc:
            eprint(f"Wiki clone failed: {exc}")
            return 1

    try:
        export_work_items(
            org=args.org,
            project=args.project,
            pat=args.pat,
            out_dir=out_dir,
            wiql=args.wiql,
            fields=args.fields,
            expand=args.expand,
            download_attachments=not args.no_attachments,
        )
    except HTTPError as exc:
        eprint(f"HTTP error: {exc.code} {exc.reason}")
        try:
            eprint(exc.read().decode("utf-8", errors="replace"))
        except Exception:
            pass
        return 1
    except URLError as exc:
        eprint(f"Network error: {exc}")
        return 1
    except Exception as exc:
        eprint(f"Unexpected error: {exc}")
        return 1

    eprint(f"Export complete. Files written to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

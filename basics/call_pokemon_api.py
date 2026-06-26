import requests


if __name__ == "__main__":
    response = requests.get("https://pokeapi.co/api/v2/pokemon/9")
    print(response.status_code)
    print(response.json()["name"])
import tkinter as tk

#Next line creates main window
root = tk.Tk()
# Widgets are added here

#Label of main window = "Title" at the top center
label = tk.Label(root, text="Hello label!")
label.pack()

#Next line starts main loop and keeps window responsive
root.mainloop()
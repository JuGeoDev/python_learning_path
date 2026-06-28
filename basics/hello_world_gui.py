import tkinter as tk

#Next line creates main window
root = tk.Tk()
#Title = Text in the top bar where the close,max,min buttons are
root.title("This title is in the top bar!")

# Widgets are added here

#Label of main window = "Title" at the top center
label = tk.Label(root, text="Hello label!")
#Label gets placed *inside* window
label.pack()

#Creates button inside the window. Args = Which window, text, size, funtion of button
button = tk.Button(root, text="Click to destroy", width=25, command=root.destroy)
button.pack()

#Next line starts main loop and keeps window responsive
root.mainloop()
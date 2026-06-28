import tkinter as tk

#Next line creates main window
root = tk.Tk()
#Title = Text in the top bar where the close,max,min buttons are
root.title("This title is in the top bar!")
#Configure window. E.g. color
root.configure(bg='lightblue')

# Widgets are added here

#Label of main window = "Title" at the top center
#label = tk.Label(root, text="Hello label!")
#Label gets placed *inside* window
#label.pack() -> However you can not use pack AND grid at the same time because then the compiler will be confused where the packed object shoulld go if not specified

#Creates button inside the window. Args = Which window, text, size, funtion of button
button = tk.Button(root, text="Click to destroy", width=25, command=root.destroy)
button.grid(row=0, column=1)
button.configure(bg='white')

#Creates labels inside window and sorts them in a grid
firstname_label = tk.Label(root, bg='white', text="First Name").grid(row=1, column=0)
lastname_label = tk.Label(root, bg='white', text="Last Name").grid(row=2, column=0)

#Accepts single line user input
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)

#Places entry fields next to labels from above in grid
entry1.grid(row=1, column=1)
entry2.grid(row=2, column=1)

#Next line starts main loop and keeps window responsive
root.mainloop()
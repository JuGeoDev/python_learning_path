import tkinter as tk

root = tk.Tk()
root.title("Calculator")
#Configure window. E.g. color
root.configure(bg='lightblue')
root_standardwidth = 5

# Widgets are added here

#Buttons 1-9
button_one = tk.Button(root, text="1", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=1)
button_two = tk.Button(root, text="2", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=2)
button_three = tk.Button(root, text="3", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=3)
button_four = tk.Button(root, text="4", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=1)
button_five = tk.Button(root, text="5", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=2)
button_six = tk.Button(root, text="6", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=3)
button_seven = tk.Button(root, text="7", bg='white', width=root_standardwidth, command=root.destroy).grid(row=3, column=1)
button_eight = tk.Button(root, text="8", bg='white', width=root_standardwidth, command=root.destroy).grid(row=3, column=2)
button_nine = tk.Button(root, text="9", bg='white', width=root_standardwidth, command=root.destroy).grid(row=3, column=3)

#Buttons operators
button_plus = tk.Button(root, text="+", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=5)
button_minus = tk.Button(root, text="-", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=6)
button_multiply = tk.Button(root, text="*", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=5)
button_divide = tk.Button(root, text="/", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=6)
button_equals = tk.Button(root, text="=", bg='white', width=root_standardwidth, command=root.destroy).grid(row=3, column=5)

#Add empty row in grid to seperate buttons from input
emptyline = tk.Label(root, width=root_standardwidth, bg='lightblue').grid(row=4, column=1)


#Creates labels inside window and sorts them in a grid
input_label = tk.Label(root, bg='white', width=10, text="Equation:").grid(row=5, column=1)

#Accepts single line user input
equation_input = tk.Entry(root, width=10).grid(row=5, column=3)

#Next line starts main loop and keeps window responsive
root.mainloop()
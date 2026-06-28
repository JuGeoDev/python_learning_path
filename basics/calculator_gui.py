import tkinter as tk

root = tk.Tk()
root.title("Calculator")
#Configure window. E.g. color
root.configure(bg='lightblue', width=100, height=100)
root_standardwidth = 5

# Widgets are added here

#Frame for calc
frame = tk.Frame(root, bg="lightgreen", width=75, height=75, bd=3, relief=tk.RIDGE)
frame.pack(padx=20, pady=20)

#Buttons 1-9
button_one = tk.Button(frame, text="1", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=1)
button_two = tk.Button(frame, text="2", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=2)
button_three = tk.Button(frame, text="3", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=3)
button_four = tk.Button(frame, text="4", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=1)
button_five = tk.Button(frame, text="5", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=2)
button_six = tk.Button(frame, text="6", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=3)
button_seven = tk.Button(frame, text="7", bg='white', width=root_standardwidth, command=root.destroy).grid(row=3, column=1)
button_eight = tk.Button(frame, text="8", bg='white', width=root_standardwidth, command=root.destroy).grid(row=3, column=2)
button_nine = tk.Button(frame, text="9", bg='white', width=root_standardwidth, command=root.destroy).grid(row=3, column=3)

#Buttons operators
button_plus = tk.Button(frame, text="+", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=5)
button_minus = tk.Button(frame, text="-", bg='white', width=root_standardwidth, command=root.destroy).grid(row=1, column=6)
button_multiply = tk.Button(frame, text="*", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=5)
button_divide = tk.Button(frame, text="/", bg='white', width=root_standardwidth, command=root.destroy).grid(row=2, column=6)
button_equals = tk.Button(frame, text="=", bg='white', width=root_standardwidth, command=root.destroy).grid(row=3, column=5)

#Add empty row in grid to seperate buttons from input
emptyline = tk.Label(frame, width=root_standardwidth, bg='lightgreen').grid(row=4, column=1)


#Creates labels inside window and sorts them in a grid
input_label = tk.Label(frame, bg='white', width=10, text="Equation:").grid(row=5, column=1)

#Accepts single line user input
equation_input = tk.Entry(frame, width=10).grid(row=5, column=3)

#Next line starts main loop and keeps window responsive
root.mainloop()
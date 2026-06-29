import tkinter as tk
import calculator_logic

root = tk.Tk()
root.title("Calculator")
#Configure window. E.g. color
root.configure(bg='#BDFCC9', width=100, height=100)
root_standardwidth = 5

#Saves buttonclick value
output= tk.StringVar(value="0")
def save_input_char(button_input):
    output.set(str(button_input))

#This will be the string from where we extract the equation
equation_expression= tk.StringVar(value="0")

# Widgets are added here

#Frame for calc
frame = tk.Frame(root, bg="plum1", width=75, height=75, bd=3, relief=tk.RIDGE)
frame.pack(padx=20, pady=20)

#Add empty row in grid at the top left
emptyline = tk.Label(frame, width=root_standardwidth, bg='#FFBBFF').grid(row=0, column=0)
#Add empty row in grid at the bottom right
emptyline = tk.Label(frame, width=root_standardwidth, bg='#FFBBFF').grid(row=6, column=7)

#Buttons 0-9
button_zero = tk.Button(frame, text="0", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(0)).grid(row=4, column=1)
button_one = tk.Button(frame, text="1", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(1)).grid(row=1, column=1)
button_two = tk.Button(frame, text="2", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(2)).grid(row=1, column=2)
button_three = tk.Button(frame, text="3", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(3)).grid(row=1, column=3)
button_four = tk.Button(frame, text="4", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(4)).grid(row=2, column=1)
button_five = tk.Button(frame, text="5", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(5)).grid(row=2, column=2)
button_six = tk.Button(frame, text="6", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(6)).grid(row=2, column=3)
button_seven = tk.Button(frame, text="7", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(7)).grid(row=3, column=1)
button_eight = tk.Button(frame, text="8", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(8)).grid(row=3, column=2)
button_nine = tk.Button(frame, text="9", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char(9)).grid(row=3, column=3)

#Buttons operators
button_plus = tk.Button(frame, text="+",font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char("+")).grid(row=1, column=5)
button_minus = tk.Button(frame, text="-", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char("-")).grid(row=1, column=6)
button_multiply = tk.Button(frame, text="*", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char("*")).grid(row=2, column=5)
button_divide = tk.Button(frame, text="/", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_input_char("/")).grid(row=2, column=6)
button_equals = tk.Button(frame, text="=", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: calculator_logic.compute_equation()).grid(row=3, column=5)

#Add empty row in grid to seperate buttons from input
emptyline = tk.Label(frame, width=root_standardwidth, bg='#FFBBFF').grid(row=5, column=1)

#Add output fields for equation and result
input_label = tk.Label(frame, font=("Comic Sans", "12"), bg="#E6FCF5", width=10, text="Equation:").grid(row=6, column=1)
result_label = tk.Label(frame, font=("Comic Sans", "12"), bg="#E6FCF5", width=10, text="Result:").grid(row=8, column=1)
#Show current input
equation_output = tk.Label(frame, font=("Comic Sans", "12"), bg= "#E6FCF5", width=20, textvariable=equation_expression)
equation_output.grid(row=6, column=3)
#Show result of equation
result_output = tk.Label(frame, font=("Comic Sans", "12"), bg= "#E6FCF5", width=20, textvariable=output)
result_output.grid(row=8, column=3)

#Add empty row in grid to seperate equation and result
emptyline = tk.Label(frame, width=root_standardwidth, bg='#FFBBFF').grid(row=7, column=1)

#Add empty row in grid to seperate result from frame
emptyline = tk.Label(frame, width=root_standardwidth, bg='#FFBBFF').grid(row=9, column=1)

#Next line starts main loop and keeps window responsive
root.mainloop()
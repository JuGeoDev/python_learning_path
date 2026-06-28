import tkinter as tk

root = tk.Tk()
root.title("Calculator")
#Configure window. E.g. color
root.configure(bg='#BDFCC9', width=100, height=100)
root_standardwidth = 5

input = 0
def save_number(button_input):
    global input
    def inner():
        global input
        input = int(button_input)
    return inner

# Widgets are added here

#Frame for calc
frame = tk.Frame(root, bg="plum1", width=75, height=75, bd=3, relief=tk.RIDGE)
frame.pack(padx=20, pady=20)

#Add empty row in grid at the top left
emptyline = tk.Label(frame, width=root_standardwidth, bg='#FFBBFF').grid(row=0, column=0)
#Add empty row in grid at the bottom right
emptyline = tk.Label(frame, width=root_standardwidth, bg='#FFBBFF').grid(row=6, column=7)

#Buttons 1-9
button_one = tk.Button(frame, text="1", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=lambda: save_number(1)).grid(row=1, column=1)
button_two = tk.Button(frame, text="2", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=save_number(2)).grid(row=1, column=2)
button_three = tk.Button(frame, text="3", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=save_number(3)).grid(row=1, column=3)
button_four = tk.Button(frame, text="4", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=save_number(4)).grid(row=2, column=1)
button_five = tk.Button(frame, text="5", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=save_number(5)).grid(row=2, column=2)
button_six = tk.Button(frame, text="6", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=save_number(6)).grid(row=2, column=3)
button_seven = tk.Button(frame, text="7", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=save_number(7)).grid(row=3, column=1)
button_eight = tk.Button(frame, text="8", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=save_number(8)).grid(row=3, column=2)
button_nine = tk.Button(frame, text="9", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=save_number(9)).grid(row=3, column=3)

#Buttons operators
button_plus = tk.Button(frame, text="+",font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=root.destroy).grid(row=1, column=5)
button_minus = tk.Button(frame, text="-", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=root.destroy).grid(row=1, column=6)
button_multiply = tk.Button(frame, text="*", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=root.destroy).grid(row=2, column=5)
button_divide = tk.Button(frame, text="/", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=root.destroy).grid(row=2, column=6)
button_equals = tk.Button(frame, text="=", font=("Comic Sans", "12"), bg='white', activebackground="#F8E7F8", width=root_standardwidth, command=root.destroy).grid(row=3, column=5)

#Add empty row in grid to seperate buttons from input
emptyline = tk.Label(frame, width=root_standardwidth, bg='#FFBBFF').grid(row=4, column=1)


#Creates labels inside window and sorts them in a grid
input_label = tk.Label(frame, font=("Comic Sans", "12"), bg="#E6FCF5", width=10, text="Result:").grid(row=5, column=1)

#Accepts single line user input
equation_output = tk.Label(frame, font=("Comic Sans", "12"), bg= "#E6FCF5", width=10, text=input).grid(row=5, column=3)

#Next line starts main loop and keeps window responsive
root.mainloop()
import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Scientific Calculator")
        self.window.geometry("400x600")
        self.window.configure(bg='#2c3e50')

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Arial', 10))
        style.configure('Display.TEntry', font=('Arial', 20))
        style.configure('Num.TButton', font=('Arial', 12, 'bold'))
        style.configure('Op.TButton', font=('Arial', 12))
        style.configure('Sci.TButton', font=('Arial', 9))

        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Display
        self.display = ttk.Entry(
            main_frame, 
            justify="right", 
            font=("Arial", 24),
            style='Display.TEntry'
        )
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=10, sticky="nsew")

        # Button frames
        scientific_frame = ttk.Frame(main_frame)
        scientific_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", pady=5)
        
        numpad_frame = ttk.Frame(main_frame)
        numpad_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=5)
        
        operations_frame = ttk.Frame(main_frame)
        operations_frame.grid(row=2, column=3, columnspan=2, sticky="nsew", pady=5)

        # Scientific buttons
        scientific_buttons = [
            'sin', 'cos', 'tan', 'log', '√',
            'x²', 'x³', 'xʸ', 'e', 'π',
            '(', ')', 'C', '⌫', '%'
        ]

        for i, button in enumerate(scientific_buttons):
            row, col = divmod(i, 5)
            cmd = lambda x=button: self.scientific_click(x)
            btn = ttk.Button(scientific_frame, text=button, command=cmd, style='Sci.TButton')
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

        # Number pad (calculator style)
        numbers = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '.'
        ]

        for i, num in enumerate(numbers):
            row, col = divmod(i, 3)
            if num == '0':  # Make 0 span two columns
                btn = ttk.Button(numpad_frame, text=num, command=lambda x=num: self.button_click(x), style='Num.TButton')
                btn.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")
            elif num == '.':
                btn = ttk.Button(numpad_frame, text=num, command=lambda x=num: self.button_click(x), style='Num.TButton')
                btn.grid(row=3, column=2, padx=2, pady=2, sticky="nsew")
            else:
                btn = ttk.Button(numpad_frame, text=num, command=lambda x=num: self.button_click(x), style='Num.TButton')
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

        # Operation buttons
        operations = ['/', '*', '-', '+', '=']
        for i, op in enumerate(operations):
            btn = ttk.Button(operations_frame, text=op, command=lambda x=op: self.button_click(x), style='Op.TButton')
            btn.grid(row=i, column=0, padx=2, pady=2, sticky="nsew")

        # Configure grid weights
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        main_frame.grid_rowconfigure(2, weight=1)
        for i in range(5):
            main_frame.grid_columnconfigure(i, weight=1)
            
        for i in range(3):
            scientific_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            scientific_frame.grid_columnconfigure(i, weight=1)
            
        for i in range(4):
            numpad_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            numpad_frame.grid_columnconfigure(i, weight=1)
            
        for i in range(5):
            operations_frame.grid_rowconfigure(i, weight=1)
        operations_frame.grid_columnconfigure(0, weight=1)

        self.current_number = ''
        self.stored_number = 0
        self.current_operation = None
        self.last_button_was_equals = False

    def scientific_click(self, operation):
        if operation == 'C':
            self.current_number = ''
            self.stored_number = 0
            self.current_operation = None
            self.display.delete(0, tk.END)
        
        elif operation == '⌫':
            if self.current_number:
                self.current_number = self.current_number[:-1]
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current_number)

        elif operation == 'π':
            self.current_number = str(math.pi)
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_number)

        elif operation == 'e':
            self.current_number = str(math.e)
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_number)

        elif operation in ['sin', 'cos', 'tan', 'log', '√', 'x²', 'x³']:
            try:
                num = float(self.current_number) if self.current_number else 0
                if operation == 'sin':
                    result = math.sin(math.radians(num))
                elif operation == 'cos':
                    result = math.cos(math.radians(num))
                elif operation == 'tan':
                    result = math.tan(math.radians(num))
                elif operation == 'log':
                    result = math.log10(num)
                elif operation == '√':
                    result = math.sqrt(num)
                elif operation == 'x²':
                    result = num ** 2
                elif operation == 'x³':
                    result = num ** 3

                self.current_number = str(result)
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current_number)
            except ValueError:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")

    def button_click(self, text):
        if self.last_button_was_equals and text.isdigit():
            self.current_number = ''
            self.last_button_was_equals = False

        if text.isdigit() or text == '.':
            self.current_number += text
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_number)
        
        elif text in ['+', '-', '*', '/']:
            if self.current_number:
                self.stored_number = float(self.current_number)
            self.current_operation = text
            self.current_number = ''
        
        elif text == '=':
            if self.current_number and self.current_operation:
                try:
                    second_number = float(self.current_number)
                    if self.current_operation == '+':
                        result = self.stored_number + second_number
                    elif self.current_operation == '-':
                        result = self.stored_number - second_number
                    elif self.current_operation == '*':
                        result = self.stored_number * second_number
                    elif self.current_operation == '/':
                        result = self.stored_number / second_number if second_number != 0 else 'Error'
                    
                    self.display.delete(0, tk.END)
                    self.display.insert(0, str(result))
                    self.current_number = str(result)
                    self.current_operation = None
                    self.last_button_was_equals = True
                except:
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Error")

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    calculator = Calculator()
    calculator.run() 
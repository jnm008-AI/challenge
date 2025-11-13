import tkinter as tk
from tkinter import ttk, messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        
        # Variables
        self.current = "0"
        self.total = 0
        self.input_value = True
        self.check_sum = False
        self.op = ""
        self.result = False
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Calculator", 
                              font=("Arial", 18, "bold"), pady=10, bg="#f0f0f0")
        title_label.pack(fill=tk.X)
        
        # Display frame
        display_frame = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=15)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.display = tk.Entry(display_frame, font=("Arial", 24, "bold"), 
                                bg="#34495e", fg="white", bd=0, 
                                insertbackground="white", justify=tk.RIGHT,
                                state="readonly", readonlybackground="#34495e")
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.config(state=tk.NORMAL)
        self.display.insert(0, "0")
        self.display.config(state=tk.DISABLED)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=10)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button configuration
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == '=':
                    btn = tk.Button(button_frame, text=text, 
                                   font=("Arial", 16, "bold"),
                                   bg="#3498db", fg="white",
                                   activebackground="#2980b9", activeforeground="white",
                                   relief=tk.RAISED, bd=2,
                                   command=lambda t=text: self.button_click(t),
                                   cursor="hand2")
                elif text in ['C', '⌫', '%']:
                    btn = tk.Button(button_frame, text=text, 
                                   font=("Arial", 14, "bold"),
                                   bg="#95a5a6", fg="white",
                                   activebackground="#7f8c8d", activeforeground="white",
                                   relief=tk.RAISED, bd=2,
                                   command=lambda t=text: self.button_click(t),
                                   cursor="hand2")
                elif text in ['+', '-', '*', '/']:
                    btn = tk.Button(button_frame, text=text, 
                                   font=("Arial", 16, "bold"),
                                   bg="#e67e22", fg="white",
                                   activebackground="#d35400", activeforeground="white",
                                   relief=tk.RAISED, bd=2,
                                   command=lambda t=text: self.button_click(t),
                                   cursor="hand2")
                elif text == '±':
                    btn = tk.Button(button_frame, text=text, 
                                   font=("Arial", 14, "bold"),
                                   bg="#95a5a6", fg="white",
                                   activebackground="#7f8c8d", activeforeground="white",
                                   relief=tk.RAISED, bd=2,
                                   command=lambda t=text: self.button_click(t),
                                   cursor="hand2")
                else:
                    btn = tk.Button(button_frame, text=text, 
                                   font=("Arial", 16, "bold"),
                                   bg="#ecf0f1", fg="#2c3e50",
                                   activebackground="#bdc3c7", activeforeground="#2c3e50",
                                   relief=tk.RAISED, bd=2,
                                   command=lambda t=text: self.button_click(t),
                                   cursor="hand2")
                
                btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        
        # Configure grid weights
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
    
    def display_update(self, value):
        self.display.config(state=tk.NORMAL)
        self.display.delete(0, tk.END)
        self.display.insert(0, value)
        self.display.config(state=tk.DISABLED)
    
    def button_click(self, char):
        if char == 'C':
            self.current = "0"
            self.total = 0
            self.input_value = True
            self.check_sum = False
            self.op = ""
            self.result = False
            self.display_update(self.current)
        
        elif char == '⌫':  # Backspace
            if len(self.current) > 1:
                self.current = self.current[:-1]
            else:
                self.current = "0"
            self.display_update(self.current)
        
        elif char == '±':  # Toggle sign
            if self.current != "0":
                if self.current[0] == '-':
                    self.current = self.current[1:]
                else:
                    self.current = '-' + self.current
                self.display_update(self.current)
        
        elif char == '%':  # Percentage
            try:
                self.current = str(float(self.current) / 100)
                self.display_update(self.current)
            except:
                self.display_update("Error")
        
        elif char in ['+', '-', '*', '/']:
            if self.check_sum:
                self.calculate()
            else:
                self.total = float(self.current)
                self.check_sum = True
            self.op = char
            self.input_value = True
            self.result = False
        
        elif char == '=':
            if self.check_sum:
                self.calculate()
            self.check_sum = False
            self.input_value = True
            self.op = ""
            self.result = True
        
        elif char == '.':
            if self.input_value:
                self.current = "0."
                self.input_value = False
            elif '.' not in self.current:
                self.current += '.'
            self.display_update(self.current)
        
        else:  # Number
            if self.input_value:
                self.current = char
                self.input_value = False
            else:
                if self.current == "0":
                    self.current = char
                else:
                    self.current += char
            self.display_update(self.current)
    
    def calculate(self):
        try:
            if self.op == '+':
                self.total += float(self.current)
            elif self.op == '-':
                self.total -= float(self.current)
            elif self.op == '*':
                self.total *= float(self.current)
            elif self.op == '/':
                if float(self.current) == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    self.current = "0"
                    self.total = 0
                    self.display_update(self.current)
                    return
                self.total /= float(self.current)
            
            # Format result
            if self.total == int(self.total):
                self.current = str(int(self.total))
            else:
                self.current = str(self.total)
            
            self.display_update(self.current)
            self.input_value = True
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            self.current = "0"
            self.total = 0
            self.display_update(self.current)

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()



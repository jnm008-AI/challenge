import tkinter as tk
from tkinter import ttk

def show_greeting():
    """Display a personalized greeting based on name and age"""
    name = name_entry.get().strip()
    age = int(age_slider.get())
    
    if name:
        greeting = f"Hello, {name}! You are {age} years old. Nice to meet you!"
    else:
        greeting = "Please enter your name!"
    
    greeting_label.config(text=greeting)

# Create the main window
root = tk.Tk()
root.title("Greetings Form")
root.geometry("400x300")
root.resizable(False, False)

# Configure style
style = ttk.Style()
style.theme_use('clam')

# Create and pack widgets
# Title
title_label = tk.Label(root, text="Welcome to the Greetings Form", 
                       font=("Arial", 16, "bold"), pady=20)
title_label.pack()

# Name entry frame
name_frame = tk.Frame(root, pady=10)
name_frame.pack()

name_label = tk.Label(name_frame, text="Name:", font=("Arial", 12))
name_label.pack(side=tk.LEFT, padx=5)

name_entry = tk.Entry(name_frame, font=("Arial", 12), width=20)
name_entry.pack(side=tk.LEFT, padx=5)

# Age slider frame
age_frame = tk.Frame(root, pady=10)
age_frame.pack()

age_label = tk.Label(age_frame, text="Age:", font=("Arial", 12))
age_label.pack(side=tk.LEFT, padx=5)

age_slider = tk.Scale(age_frame, from_=1, to=120, orient=tk.HORIZONTAL, 
                      length=200, font=("Arial", 10))
age_slider.set(25)  # Default age
age_slider.pack(side=tk.LEFT, padx=5)

# Age value display
age_value_label = tk.Label(age_frame, text="25", font=("Arial", 10, "bold"), 
                           width=3)
age_value_label.pack(side=tk.LEFT, padx=5)

# Update age display when slider moves
def update_age_display(value):
    age_value_label.config(text=str(int(float(value))))

age_slider.config(command=update_age_display)

# Submit button
submit_button = tk.Button(root, text="Show Greeting", command=show_greeting,
                          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                          padx=20, pady=10, cursor="hand2")
submit_button.pack(pady=20)

# Greeting display label
greeting_label = tk.Label(root, text="", font=("Arial", 11), 
                          wraplength=350, justify=tk.CENTER, 
                          fg="#333333", pady=10)
greeting_label.pack()

# Run the application
root.mainloop()


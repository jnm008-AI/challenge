import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

class ExpenseSplitter:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Splitter - Friends Trip")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Data storage
        self.friends = []
        self.expenses = []
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="💰 Expense Splitter for Friends Trip", 
                               font=("Arial", 18, "bold"), pady=15, bg="#f0f0f0")
        title_label.pack(fill=tk.X)
        
        # Main container with notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Add Friends
        friends_frame = ttk.Frame(notebook)
        notebook.add(friends_frame, text="👥 Friends")
        self.create_friends_tab(friends_frame)
        
        # Tab 2: Add Expenses
        expenses_frame = ttk.Frame(notebook)
        notebook.add(expenses_frame, text="💸 Expenses")
        self.create_expenses_tab(expenses_frame)
        
        # Tab 3: Summary & Settlements
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="📊 Summary")
        self.create_summary_tab(summary_frame)
        
    def create_friends_tab(self, parent):
        # Add friend section
        add_frame = tk.Frame(parent, pady=20)
        add_frame.pack()
        
        tk.Label(add_frame, text="Add Friend:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.friend_entry = tk.Entry(add_frame, font=("Arial", 12), width=20)
        self.friend_entry.pack(side=tk.LEFT, padx=5)
        self.friend_entry.bind('<Return>', lambda e: self.add_friend())
        
        add_btn = tk.Button(add_frame, text="Add", command=self.add_friend,
                           font=("Arial", 11), bg="#4CAF50", fg="white",
                           padx=15, pady=5, cursor="hand2")
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Friends list
        list_frame = tk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(list_frame, text="Friends List:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.friends_listbox = tk.Listbox(list_frame, font=("Arial", 11), 
                                          yscrollcommand=scrollbar.set, height=15)
        self.friends_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.friends_listbox.yview)
        
        # Remove friend button
        remove_btn = tk.Button(list_frame, text="Remove Selected", 
                              command=self.remove_friend,
                              font=("Arial", 10), bg="#f44336", fg="white",
                              padx=10, pady=5, cursor="hand2")
        remove_btn.pack(pady=10)
        
    def create_expenses_tab(self, parent):
        # Expense form
        form_frame = tk.LabelFrame(parent, text="Add New Expense", 
                                   font=("Arial", 12, "bold"), pady=15, padx=15)
        form_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Description
        desc_frame = tk.Frame(form_frame)
        desc_frame.pack(fill=tk.X, pady=5)
        tk.Label(desc_frame, text="Description:", font=("Arial", 11), width=12, anchor=tk.W).pack(side=tk.LEFT)
        self.expense_desc = tk.Entry(desc_frame, font=("Arial", 11), width=30)
        self.expense_desc.pack(side=tk.LEFT, padx=5)
        
        # Amount
        amount_frame = tk.Frame(form_frame)
        amount_frame.pack(fill=tk.X, pady=5)
        tk.Label(amount_frame, text="Amount ($):", font=("Arial", 11), width=12, anchor=tk.W).pack(side=tk.LEFT)
        self.expense_amount = tk.Entry(amount_frame, font=("Arial", 11), width=30)
        self.expense_amount.pack(side=tk.LEFT, padx=5)
        
        # Paid by
        paid_frame = tk.Frame(form_frame)
        paid_frame.pack(fill=tk.X, pady=5)
        tk.Label(paid_frame, text="Paid By:", font=("Arial", 11), width=12, anchor=tk.W).pack(side=tk.LEFT)
        self.paid_by_var = tk.StringVar()
        self.paid_by_combo = ttk.Combobox(paid_frame, textvariable=self.paid_by_var, 
                                          font=("Arial", 11), width=27, state="readonly")
        self.paid_by_combo.pack(side=tk.LEFT, padx=5)
        
        # Split between
        split_frame = tk.Frame(form_frame)
        split_frame.pack(fill=tk.X, pady=5)
        tk.Label(split_frame, text="Split Between:", font=("Arial", 11), width=12, anchor=tk.W).pack(side=tk.LEFT)
        
        self.split_check_frame = tk.Frame(split_frame)
        self.split_check_frame.pack(side=tk.LEFT, padx=5)
        self.split_checkboxes = {}
        
        # Add expense button
        add_expense_btn = tk.Button(form_frame, text="Add Expense", 
                                    command=self.add_expense,
                                    font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                                    padx=20, pady=8, cursor="hand2")
        add_expense_btn.pack(pady=15)
        
        # Expenses list
        expenses_list_frame = tk.LabelFrame(parent, text="Expenses History", 
                                            font=("Arial", 12, "bold"), pady=10, padx=15)
        expenses_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview for expenses
        columns = ("Description", "Amount", "Paid By", "Split Between")
        self.expenses_tree = ttk.Treeview(expenses_list_frame, columns=columns, 
                                         show="headings", height=10)
        
        for col in columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, width=150)
        
        scrollbar_exp = tk.Scrollbar(expenses_list_frame, orient=tk.VERTICAL, 
                                     command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscrollcommand=scrollbar_exp.set)
        
        self.expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_exp.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Remove expense button
        remove_exp_btn = tk.Button(expenses_list_frame, text="Remove Selected", 
                                   command=self.remove_expense,
                                   font=("Arial", 10), bg="#f44336", fg="white",
                                   padx=10, pady=5, cursor="hand2")
        remove_exp_btn.pack(pady=5)
        
    def create_summary_tab(self, parent):
        # Summary display
        summary_text_frame = tk.LabelFrame(parent, text="Settlement Summary", 
                                           font=("Arial", 12, "bold"), pady=10, padx=15)
        summary_text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        scrollbar_sum = tk.Scrollbar(summary_text_frame)
        scrollbar_sum.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.summary_text = tk.Text(summary_text_frame, font=("Arial", 11), 
                                    yscrollcommand=scrollbar_sum.set, wrap=tk.WORD)
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_sum.config(command=self.summary_text.yview)
        
        # Calculate button
        calc_btn = tk.Button(parent, text="Calculate Settlements", 
                            command=self.calculate_settlements,
                            font=("Arial", 14, "bold"), bg="#FF9800", fg="white",
                            padx=30, pady=10, cursor="hand2")
        calc_btn.pack(pady=15)
        
    def add_friend(self):
        name = self.friend_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a friend's name!")
            return
        
        if name in self.friends:
            messagebox.showwarning("Warning", f"{name} is already in the list!")
            return
        
        self.friends.append(name)
        self.friends_listbox.insert(tk.END, name)
        self.friend_entry.delete(0, tk.END)
        self.update_expense_ui()
        
    def remove_friend(self):
        selection = self.friends_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a friend to remove!")
            return
        
        index = selection[0]
        friend = self.friends_listbox.get(index)
        self.friends.remove(friend)
        self.friends_listbox.delete(index)
        self.update_expense_ui()
        # Remove expenses involving this friend
        self.expenses = [exp for exp in self.expenses if exp['paid_by'] != friend and friend not in exp['split_between']]
        self.refresh_expenses_display()
        
    def update_expense_ui(self):
        # Update paid by combobox
        self.paid_by_combo['values'] = self.friends
        
        # Update split checkboxes
        for checkbox, var in self.split_checkboxes.values():
            checkbox.destroy()
        self.split_checkboxes.clear()
        
        if hasattr(self, 'split_check_frame'):
            for friend in self.friends:
                var = tk.BooleanVar()
                var.set(True)  # Default: all friends split
                checkbox = tk.Checkbutton(self.split_check_frame, text=friend, 
                                          variable=var, font=("Arial", 10))
                checkbox.pack(anchor=tk.W)
                self.split_checkboxes[friend] = (checkbox, var)
        
    def add_expense(self):
        if not self.friends:
            messagebox.showwarning("Warning", "Please add friends first!")
            return
        
        desc = self.expense_desc.get().strip()
        if not desc:
            messagebox.showwarning("Warning", "Please enter expense description!")
            return
        
        try:
            amount = float(self.expense_amount.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount!")
            return
        
        paid_by = self.paid_by_var.get()
        if not paid_by:
            messagebox.showwarning("Warning", "Please select who paid!")
            return
        
        # Get split between friends
        split_between = [friend for friend, (_, var) in self.split_checkboxes.items() 
                        if var.get()]
        
        if not split_between:
            messagebox.showwarning("Warning", "Please select at least one person to split with!")
            return
        
        # Add expense
        expense = {
            'description': desc,
            'amount': amount,
            'paid_by': paid_by,
            'split_between': split_between
        }
        self.expenses.append(expense)
        
        # Clear form
        self.expense_desc.delete(0, tk.END)
        self.expense_amount.delete(0, tk.END)
        self.paid_by_var.set('')
        
        # Refresh display
        self.refresh_expenses_display()
        
    def refresh_expenses_display(self):
        # Clear treeview
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        # Add expenses
        for expense in self.expenses:
            split_str = ", ".join(expense['split_between'])
            self.expenses_tree.insert("", tk.END, values=(
                expense['description'],
                f"${expense['amount']:.2f}",
                expense['paid_by'],
                split_str
            ))
    
    def remove_expense(self):
        selection = self.expenses_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an expense to remove!")
            return
        
        item = selection[0]
        index = self.expenses_tree.index(item)
        self.expenses.pop(index)
        self.refresh_expenses_display()
        
    def calculate_settlements(self):
        if not self.friends:
            messagebox.showwarning("Warning", "Please add friends first!")
            return
        
        if not self.expenses:
            messagebox.showwarning("Warning", "No expenses to calculate!")
            return
        
        # Calculate net balance for each person
        balances = defaultdict(float)
        
        for expense in self.expenses:
            amount = expense['amount']
            paid_by = expense['paid_by']
            split_between = expense['split_between']
            
            # Person who paid gets credited
            balances[paid_by] += amount
            
            # People who split get debited
            per_person = amount / len(split_between)
            for person in split_between:
                balances[person] -= per_person
        
        # Calculate who owes whom
        creditors = {}  # People who are owed money
        debtors = {}    # People who owe money
        
        for person, balance in balances.items():
            if balance > 0.01:  # Small threshold for floating point
                creditors[person] = balance
            elif balance < -0.01:
                debtors[person] = abs(balance)
        
        # Generate summary
        summary = "=" * 60 + "\n"
        summary += "EXPENSE SPLITTER SUMMARY\n"
        summary += "=" * 60 + "\n\n"
        
        # Total expenses
        total = sum(exp['amount'] for exp in self.expenses)
        summary += f"Total Expenses: ${total:.2f}\n"
        summary += f"Number of Expenses: {len(self.expenses)}\n\n"
        
        # Individual balances
        summary += "-" * 60 + "\n"
        summary += "INDIVIDUAL BALANCES:\n"
        summary += "-" * 60 + "\n"
        for person in sorted(self.friends):
            balance = balances.get(person, 0)
            if abs(balance) < 0.01:
                summary += f"{person:20s}: $0.00 (Settled)\n"
            elif balance > 0:
                summary += f"{person:20s}: +${balance:.2f} (Should receive)\n"
            else:
                summary += f"{person:20s}: -${abs(balance):.2f} (Should pay)\n"
        
        # Settlements needed
        summary += "\n" + "-" * 60 + "\n"
        summary += "SETTLEMENTS NEEDED:\n"
        summary += "-" * 60 + "\n"
        
        if not debtors or not creditors:
            summary += "All expenses are already settled! 🎉\n"
        else:
            # Simple settlement algorithm
            settlements = []
            debtors_list = sorted(debtors.items(), key=lambda x: x[1], reverse=True)
            creditors_list = sorted(creditors.items(), key=lambda x: x[1], reverse=True)
            
            i, j = 0, 0
            while i < len(debtors_list) and j < len(creditors_list):
                debtor, debt = debtors_list[i]
                creditor, credit = creditors_list[j]
                
                if debt <= credit:
                    settlements.append((debtor, creditor, debt))
                    creditors_list[j] = (creditor, credit - debt)
                    i += 1
                    if creditors_list[j][1] < 0.01:
                        j += 1
                else:
                    settlements.append((debtor, creditor, credit))
                    debtors_list[i] = (debtor, debt - credit)
                    j += 1
            
            for debtor, creditor, amount in settlements:
                summary += f"{debtor:20s} → {creditor:20s}: ${amount:.2f}\n"
        
        summary += "\n" + "=" * 60 + "\n"
        
        # Display summary
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary)
        self.summary_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = ExpenseSplitter(root)
    root.mainloop()

if __name__ == "__main__":
    main()


import random
import tkinter as tk
from tkinter import messagebox, ttk

# Custom Exception Classes
class InvalidInputError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, account_id, passcode, account_category, funds=0):
        self.account_id = account_id
        self.passcode = passcode
        self.account_category = account_category
        self.funds = funds
        
    def deposit(self, amount):
        """Deposit money into account"""
        if amount > 0:
            self.funds += amount
            return True
        raise InvalidInputError("Invalid deposit amount")
        
    def withdraw(self, amount):
        """Withdraw money from account"""
        if amount <= 0:
            raise InvalidInputError("Invalid withdrawal amount")
        if amount > self.funds:
            raise InsufficientFundsError("Insufficient funds")
        self.funds -= amount
        return True
        
    def transfer(self, amount, recipient):
        """Transfer money to another account"""
        self.withdraw(amount)
        recipient.deposit(amount)
        return True
        
    def mobile_topup(self, amount, mobile_number):
        """Top up mobile phone balance"""
        if (not mobile_number.isdigit() or 
        len(mobile_number) != 8 or 
        (not mobile_number.startswith('17') and not mobile_number.startswith('77'))):
            raise InvalidInputError("Invalid mobile number")
        self.withdraw(amount)
        return True
            
    def change_password(self, new_passcode):
        """Change account password"""
        if len(new_passcode) != 4 or not new_passcode.isdigit():
            raise InvalidInputError("Passcode must be 4 digits")
        self.passcode = new_passcode
        return True

class BankingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking App")
        self.root.geometry("500x500")
        self.font = ("Arial", 12)
        
        self.accounts = {}
        self.current_account = None
        
        self.show_main_menu()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        self.clear_frame()
        self.current_account = None
        
        tk.Label(self.root, text="Banking App", font=("Arial", 16)).pack(pady=20)
        
        buttons = [
            ("Create Account", self.show_create_account),
            ("Login", self.show_login),
            ("Exit", self.root.quit)
        ]
        
        for text, cmd in buttons:
            tk.Button(self.root, text=text, command=cmd, **self.button_style()).pack(pady=5)
    
    def button_style(self):
        return {'font': self.font, 'width': 20}
    
    def show_create_account(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Create Account", font=("Arial", 14)).pack(pady=10)
        
        self.account_type = tk.StringVar(value="Personal")
        tk.Radiobutton(self.root, text="Personal", variable=self.account_type, 
                      value="Personal", font=self.font).pack()
        tk.Radiobutton(self.root, text="Business", variable=self.account_type, 
                      value="Business", font=self.font).pack(pady=5)
        
        tk.Button(self.root, text="Create", command=self.create_account, **self.button_style()).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_menu, **self.button_style()).pack()
    
    def create_account(self):
        account_id = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))
        
        if self.account_type.get() == "Personal":
            account = BankAccount(account_id, passcode, "Personal")
        else:
            account = BankAccount(account_id, passcode, "Business")
        
        self.accounts[account_id] = account
        messagebox.showinfo("Success", f"Account Created!\nID: {account_id}\nPasscode: {passcode}")
        self.show_main_menu()
    
    def show_login(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Login", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="Account ID:", font=self.font).pack()
        self.login_id = tk.Entry(self.root, font=self.font)
        self.login_id.pack(pady=5)
        
        tk.Label(self.root, text="Passcode:", font=self.font).pack()
        self.login_pass = tk.Entry(self.root, font=self.font, show="*")
        self.login_pass.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.login, **self.button_style()).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_menu, **self.button_style()).pack()
    
    def login(self):
        account_id = self.login_id.get()
        passcode = self.login_pass.get()
        
        if account_id in self.accounts and self.accounts[account_id].passcode == passcode:
            self.current_account = self.accounts[account_id]
            self.show_account_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def show_account_menu(self):
        self.clear_frame()
        
        tk.Label(self.root, text=f"Welcome {self.current_account.account_id}", 
                font=("Arial", 14)).pack(pady=10)
        
        options = [
            ("Check Balance", self.show_balance),
            ("Deposit", self.show_deposit),
            ("Withdraw", self.show_withdraw),
            ("Transfer", self.show_transfer),
            ("Mobile Top-Up", self.show_mobile_topup),
            ("Change Password", self.show_change_password),
            ("Logout", self.show_main_menu)
        ]
        
        for text, cmd in options:
            tk.Button(self.root, text=text, command=cmd, **self.button_style()).pack(pady=3)
    
    def show_balance(self):
        self.clear_frame()
        
        tk.Label(self.root, text=f"Current Balance: ${self.current_account.funds:.2f}", 
                font=self.font).pack(pady=20)
        
        tk.Button(self.root, text="Back", command=self.show_account_menu, **self.button_style()).pack()
    
    def show_deposit(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Deposit Amount", font=("Arial", 14)).pack(pady=10)
        
        self.amount_entry = tk.Entry(self.root, font=self.font)
        self.amount_entry.pack(pady=10)
        
        tk.Button(self.root, text="Submit", command=self.do_deposit, **self.button_style()).pack()
        tk.Button(self.root, text="Back", command=self.show_account_menu, **self.button_style()).pack()
    
    def do_deposit(self):
        try:
            amount = float(self.amount_entry.get())
            self.current_account.deposit(amount)
            messagebox.showinfo("Success", "Deposit completed")
            self.show_account_menu()
        except InvalidInputError:
            messagebox.showerror("Error", "Invalid amount")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")
    
    def show_withdraw(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Withdraw Amount", font=("Arial", 14)).pack(pady=10)
        
        self.amount_entry = tk.Entry(self.root, font=self.font)
        self.amount_entry.pack(pady=10)
        
        tk.Button(self.root, text="Submit", command=self.do_withdraw, **self.button_style()).pack()
        tk.Button(self.root, text="Back", command=self.show_account_menu, **self.button_style()).pack()
    
    def do_withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            self.current_account.withdraw(amount)
            messagebox.showinfo("Success", "Withdrawal completed")
            self.show_account_menu()
        except InvalidInputError:
            messagebox.showerror("Error", "Invalid amount")
        except InsufficientFundsError:
            messagebox.showerror("Error", "Insufficient funds")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")
    
    def show_transfer(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Transfer Funds", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="Recipient Account ID:", font=self.font).pack()
        self.recipient_entry = tk.Entry(self.root, font=self.font)
        self.recipient_entry.pack(pady=5)
        
        tk.Label(self.root, text="Amount:", font=self.font).pack()
        self.amount_entry = tk.Entry(self.root, font=self.font)
        self.amount_entry.pack(pady=5)
        
        tk.Button(self.root, text="Submit", command=self.do_transfer, **self.button_style()).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_account_menu, **self.button_style()).pack()
    
    def do_transfer(self):
        try:
            recipient_id = self.recipient_entry.get()
            amount = float(self.amount_entry.get())
            
            if recipient_id not in self.accounts:
                raise InvalidInputError("Recipient account not found")
                
            self.current_account.transfer(amount, self.accounts[recipient_id])
            messagebox.showinfo("Success", "Transfer completed")
            self.show_account_menu()
        except (InvalidInputError, InsufficientFundsError) as e:
            messagebox.showerror("Error", str(e))
        except ValueError:
            messagebox.showerror("Error", "Enter valid details")
    
    def show_mobile_topup(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Mobile Top-Up", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="Mobile Number:", font=self.font).pack()
        self.mobile_entry = tk.Entry(self.root, font=self.font)
        self.mobile_entry.pack(pady=5)
        
        tk.Label(self.root, text="Amount:", font=self.font).pack()
        self.amount_entry = tk.Entry(self.root, font=self.font)
        self.amount_entry.pack(pady=5)
        
        tk.Button(self.root, text="Submit", command=self.do_mobile_topup, **self.button_style()).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_account_menu, **self.button_style()).pack()
    
    def do_mobile_topup(self):
        try:
            mobile = self.mobile_entry.get()
            amount = float(self.amount_entry.get())
            self.current_account.mobile_topup(amount, mobile)
            messagebox.showinfo("Success", f"${amount} credited to {mobile}")
            self.show_account_menu()
        except (InvalidInputError, InsufficientFundsError) as e:
            messagebox.showerror("Error", str(e))
        except ValueError:
            messagebox.showerror("Error", "Enter valid details")
    
    def show_change_password(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Change Password", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.root, text="New 4-digit Passcode:", font=self.font).pack()
        self.new_pass_entry = tk.Entry(self.root, font=self.font, show="*")
        self.new_pass_entry.pack(pady=5)
        
        tk.Label(self.root, text="Confirm Passcode:", font=self.font).pack()
        self.confirm_pass_entry = tk.Entry(self.root, font=self.font, show="*")
        self.confirm_pass_entry.pack(pady=5)
        
        tk.Button(self.root, text="Submit", command=self.do_change_password, **self.button_style()).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_account_menu, **self.button_style()).pack()
    
    def do_change_password(self):
        try:
            new_pass = self.new_pass_entry.get()
            confirm_pass = self.confirm_pass_entry.get()
            
            if new_pass != confirm_pass:
                raise InvalidInputError("Passcodes don't match")
                
            self.current_account.change_password(new_pass)
            messagebox.showinfo("Success", "Password changed successfully")
            self.show_account_menu()
        except InvalidInputError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()
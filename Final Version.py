############### IMPORTS ###############
import tkinter as tk
from tkinter import *
from tkinter import ttk


############### CLASSES ###############
# Account class
class Account:
    def __init__(self, name, balance, bonus):
        self.name = name
        self.balance = float(balance)
        self.bonus = float(bonus)
        account_list.append(self)

# Withdraw method subtracts money from their allowance
    def withdraw(self, amount):
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            return True
        else:
            return False


class WindowStyle:
    def __init__(self, master):
        self.master = master
        style = ttk.Style()
        style.theme_use("xpnative")


############### FUNCTIONS AND SETUP ###############
# Function for reading in account names and info from file
def accounts_data():
    account_file = open("child_accounts.txt", "r")
    line_list = account_file.readlines()

    for line in line_list:
        account_data = line.strip().split(",")
        Account(*account_data)

    account_file.close()


# A function to get account names list
def account_names_list():
    name_list = []
    for account in account_list:
        name_list.append(account.name)
    return name_list


# A function that will update the balance.
def balance_updates():
    balance_string = ""
    account_file = open("child_accounts.txt", "w")
    # Append each accounts balance, progress and bonus to the label
    for account in account_list:
        if account.balance > account.bonus:
            balance_string += "{}: ${:.2f}. On track to recieve bonus.\n".format(account.name, account.balance)
            account_file.write("{},{},{}\n".format(account.name, account.balance, account.bonus))
        else:
            balance_string += "{}: ${:.2f}. Not on track to recieve the bonus.\n".format(account.name, account.balance)
            account_file.write("{},{},{}\n".format(account.name, account.balance, account.bonus))
    account_information.set(balance_string)
    account_file.close()


# Withdraw function
def withdraw_money(account):
    if account.withdraw(amount.get()):
        action_feedback.set("Success! Total of ${:.2f} withdrawn from {}".format(amount.get(), account.name))
    else:
        action_feedback.set("Not enough money in account or not a valid amount".format(account.name))


# Manage action function
def manage_action():
    try:
        for account in account_list:
            if chosen_account.get() == account.name:
                withdraw_money(account)

        # Update the GUI
        balance_updates()
        amount.set("")

    # Exception for text input
    except Exception:
        action_feedback.set("Please enter a valid number")


# Lists
account_list = []

# Instances of the class
accounts_data()
account_names = account_names_list()

############### GUI CODE ###############
root = tk.Tk()
root.configure(bg="grey")
window = WindowStyle(root)
root.title("Clothing Allowance")

# Top frame
top_frame = ttk.LabelFrame(root, text="Account Information")
top_frame.grid(row=0, column=0, padx=25, pady=25, sticky="NSEW")

# Set the message text variable
message_text = StringVar()
message_text.set("Ranui Family Clothing Allowance app!")

# Pack the message label
message_label = ttk.Label(top_frame, textvariable=message_text, wraplength=250, foreground="blue", justify="right")
message_label.grid(row=0, column=0, columnspan=2, padx=25, pady=25)

# Set the account details variable
account_information = StringVar()

# Details label and pack it into the GUI
details_label = ttk.Label(top_frame, textvariable=account_information, justify="left")
details_label.grid(row=2, column=0, columnspan=2, padx=25, pady=25)

# Bottom frame
bottom_frame = ttk.LabelFrame(root)
bottom_frame.grid(row=1, column=0, padx=25, pady=25, sticky="NSEW")

# A label for the account combobox
account_label = ttk.Label(bottom_frame, text="Account: ", foreground="blue")
account_label.grid(row=3, column=0, padx=25, pady=3)

# Set up a variable and option list for the account Combobox
chosen_account = StringVar()
chosen_account.set(account_names[0])

# Combobox to select the account
account_box = ttk.Combobox(bottom_frame, textvariable=chosen_account, state="readonly")
account_box['values'] = account_names
account_box.grid(row=3, column=1, padx=25, pady=3, sticky="WE")

# Label for Amount
amount_label = ttk.Label(bottom_frame, text="Amount:", foreground="blue")
amount_label.grid(row=5, column=0, padx=25, pady=3)

# Variable used to store an amount
amount = DoubleVar()
amount.set("")

# Entry Amount
amount_entry = ttk.Entry(bottom_frame, textvariable=amount)
amount_entry.grid(row=5, column=1, padx=25, pady=3, sticky="WE")

# Submit Button
submit_button = ttk.Button(bottom_frame, text="Submit", command=manage_action)
submit_button.grid(row=6, column=0, columnspan=2, padx=25, pady=25)

# Gives feedback based on the value submitted
action_feedback = StringVar()
action_feedback_label = ttk.Label(bottom_frame, textvariable=action_feedback, foreground="red")
action_feedback_label.grid(row=7, column=0, columnspan=2)

# Runs the mainloop
balance_updates()
root.mainloop()

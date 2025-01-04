import os
import hashlib
import datetime

# Constants
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_account():
    print("\n--- Create Account ---")
    name = input("Enter your name: ")
    while True:
        try:
            initial_deposit = float(input("Enter your initial deposit: "))
            if initial_deposit < 0:
                raise ValueError("Deposit must be non-negative.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
    
    password = hash_password(input("Enter a password: "))
    account_number = str(hashlib.md5((name + str(datetime.datetime.now())).encode()).hexdigest()[:6])

    # Save account details
    with open(ACCOUNTS_FILE, "a") as f:
        f.write(f"{account_number},{name},{password},{initial_deposit}\n")

    print(f"Account created successfully! Your account number is: {account_number}")

def login():
    print("\n--- Login ---")
    account_number = input("Enter your account number: ")
    password = hash_password(input("Enter your password: "))

    with open(ACCOUNTS_FILE, "r") as f:
        for line in f:
            acc_no, name, hashed_pwd, balance = line.strip().split(",")
            if acc_no == account_number and hashed_pwd == password:
                print(f"Login successful! Welcome, {name}.")
                return account_number, name, float(balance)

    print("Invalid account number or password.")
    return None, None, None

def deposit(account_number, current_balance):
    while True:
        try:
            amount = float(input("Enter amount to deposit: "))
            if amount <= 0:
                raise ValueError("Deposit amount must be greater than zero.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    current_balance += amount
    log_transaction(account_number, "Deposit", amount)
    print(f"Deposit successful! Current balance: {current_balance}")
    update_account_balance(account_number, current_balance)


def withdraw(account_number, current_balance):
    while True:
        try:
            amount = float(input("Enter amount to withdraw: "))
            if amount <= 0:
                raise ValueError("Withdrawal amount must be greater than zero.")
            if amount > current_balance:
                raise ValueError("Insufficient balance.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    current_balance -= amount
    update_account_balance(account_number, current_balance)
    log_transaction(account_number, "Withdrawal", amount)
    print(f"Withdrawal successful! Current balance: {current_balance}")

def update_account_balance(account_number, new_balance):
    lines = []
    with open(ACCOUNTS_FILE, "r") as f:
        lines = f.readlines()

    with open(ACCOUNTS_FILE, "w") as f:
        for line in lines:
            acc_no, name, hashed_pwd, balance = line.strip().split(",")
            if acc_no == account_number:
                f.write(f"{acc_no},{name},{hashed_pwd},{new_balance}\n")
            else:
                f.write(line)

def log_transaction(account_number, transaction_type, amount):
    with open(TRANSACTIONS_FILE, "a") as f:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{account_number},{transaction_type},{amount},{date}\n")

def main_menu():
    while True:
        print("\n--- Banking System ---")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            account_number, name, balance = login()
            if account_number:
                user_menu(account_number, balance)
        elif choice == "3":
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(account_number, current_balance):
    while True:
        print("\n--- Account Menu ---")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            deposit(account_number, current_balance)
        elif choice == "2":
            withdraw(account_number, current_balance)
        elif choice == "3":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if not os.path.exists(ACCOUNTS_FILE):
        open(ACCOUNTS_FILE, "w").close()

    if not os.path.exists(TRANSACTIONS_FILE):
        open(TRANSACTIONS_FILE, "w").close()

    main_menu()

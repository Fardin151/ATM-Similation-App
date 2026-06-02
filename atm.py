class ATM:
    def __init__(self, balance=0):
        self.balance = balance

    def check_balance(self):
        print(f"\nYour current balance is: ${self.balance:.2f}")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"\nSuccessfully deposited ${amount:.2f}")
        else:
            print("\nInvalid deposit amount")

    def withdraw(self, amount):
        if amount <= 0:
            print("\nInvalid withdrawal amount")
        elif amount > self.balance:
            print("\nInsufficient balance")
        else:
            self.balance -= amount
            print(f"\nSuccessfully withdrew ${amount:.2f}")


# Menu function (OUTSIDE the class)
def atm_menu():
    print("\nWelcome to the ATM!")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")


def main():
    atm = ATM(0)

    while True:
        atm_menu()
        choice = input("Please choose an option: ")

        if choice == "1":
            atm.check_balance()

        elif choice == "2":
            amount = float(input("Enter the amount to deposit: "))
            atm.deposit(amount)

        elif choice == "3":
            amount = float(input("Enter the amount to withdraw: "))
            atm.withdraw(amount)

        elif choice == "4":
            print("\nThank you for using the ATM. Goodbye!")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()
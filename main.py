from modules.user_manager import UserManager

from modules.user_manager import UserManager
from modules.transaction_manager import TransactionManager
import os


class FinanceApp:
    """Main application class for Personal Finance Manager."""

    def __init__(self):
        """Initialize the app with a UserManager."""
        self.user_manager = UserManager()
        self.current_user = None
        self.transaction_manager = None

    def show_main_menu(self):
        """Display the main menu and return the user's choice."""
        print("\n===== Personal Finance Manager =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        return input("Choose an option: ").strip()

    def show_transaction_menu(self):
        """Show the transaction menu after login."""
        print("\n===== Transaction Menu =====")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Logout")
        return input("Choose an option: ").strip()

    # -------------------- MAIN LOOP --------------------
    def run(self):
        """Run the main application loop."""
        while True:
            choice = self.show_main_menu()

            if choice == "1":
                try:
                    user = self.user_manager.register_user()
                    if user:
                        print(f"You are now registered as {user.name}.")
                except Exception as e:
                    print(f"Error during registration: {e}")

            elif choice == "2":
                try:
                    user = self.user_manager.login_user()
                    if user:
                        self.current_user = user
                        print(f"You are now logged in as {user.name}.")
                        self.load_user_transactions()
                        self.transaction_loop()
                except Exception as e:
                    print(f"Error during login: {e}")

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

    # -------------------- LOAD USER TRANSACTION FILE --------------------
    def load_user_transactions(self):
        """Load or create the transaction CSV file for the logged-in user."""
        username = self.current_user.name
        user_id = self.current_user.user_id
        base_dir = "database"
        user_folder = f"{username}_{user_id[:8]}".replace(" ", "_")
        csv_path = os.path.join(base_dir, user_folder, "transactions.csv")

        self.transaction_manager = TransactionManager(csv_path)

    # -------------------- TRANSACTION LOOP --------------------
    def transaction_loop(self):
        """Run transaction menu for the logged-in user."""
        while True:
            choice = self.show_transaction_menu()

            if choice == "1":
                t_type = input("Enter transaction type (Income/Expense): ").strip()
                category = input("Enter category: ").strip()
                amount = input("Enter amount: ").strip()
                self.transaction_manager.add_transaction(t_type, category, amount)

            elif choice == "2":
                self.transaction_manager.list_transactions()

            elif choice == "3":
                self.transaction_manager.list_transactions()
                try:
                    index = int(input("Enter transaction number to edit: "))
                    new_type = input("New Type (leave empty to skip): ").strip() or None
                    new_category = (
                        input("New Category (leave empty to skip): ").strip() or None
                    )
                    new_amount = (
                        input("New Amount (leave empty to skip): ").strip() or None
                    )
                    self.transaction_manager.edit_transaction(
                        index, new_type, new_category, new_amount
                    )
                except ValueError:
                    print("Invalid number. Try again.")

            elif choice == "4":
                self.transaction_manager.list_transactions()
                try:
                    index = int(input("Enter transaction number to delete: "))
                    self.transaction_manager.delete_transaction(index)
                except ValueError:
                    print("Invalid number. Try again.")

            elif choice == "5":
                print(f"Logging out {self.current_user.name}...")
                self.current_user = None
                break

            else:
                print("Invalid choice. Please try again.")


def main():
    """Main entry point."""
    app = FinanceApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting program.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

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

    # -------------------- MAIN MENU --------------------
    def show_main_menu(self):
        """Display the main menu."""
        print("\n===== Personal Finance Manager =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()
        while choice not in ["1", "2", "3"]:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
            choice = input("Choose an option: ").strip()
        return choice

    # -------------------- TRANSACTION MENU --------------------
    def show_transaction_menu(self):
        """Show the transaction menu after login."""
        print("\n===== Transaction Menu =====")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Logout")

        choice = input("Choose an option: ").strip()
        while choice not in ["1", "2", "3", "4", "5"]:
            print("❌ Invalid choice. Please enter 1–5.")
            choice = input("Choose an option: ").strip()
        return choice

    # -------------------- MAIN LOOP --------------------
    def run(self):
        """Run the main application loop."""
        while True:
            choice = self.show_main_menu()

            if choice == "1":
                self.register_flow()

            elif choice == "2":
                self.login_flow()

            elif choice == "3":
                print("👋 Goodbye!")
                break

    # -------------------- REGISTER --------------------
    def register_flow(self):
        try:
            user = self.user_manager.register_user()
            if user:
                print(f"✅ You are now registered as {user.name}.")
        except Exception as e:
            print(f"Error during registration: {e}")

    # -------------------- LOGIN --------------------
    def login_flow(self):
        try:
            user = self.user_manager.login_user()
            if user:
                self.current_user = user
                print(f"✅ Logged in as {user.name}.")
                self.load_user_transactions()
                self.transaction_loop()
        except Exception as e:
            print(f"Error during login: {e}")

    # -------------------- LOAD USER TRANSACTIONS --------------------
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
        """Run the transaction menu for the logged-in user."""
        while True:
            choice = self.show_transaction_menu()

            if choice == "1":
                self.transaction_manager.add_transaction()

            elif choice == "2":
                self.transaction_manager.list_transactions()

            elif choice == "3":
                self.transaction_manager.list_transactions()
                try:
                    index = int(input("\nEnter transaction number to edit: ").strip())
                    self.transaction_manager.edit_transaction(index)
                except ValueError:
                    print("❌ Invalid input. Please enter a number.")
                except Exception as e:
                    print(f"Error editing transaction: {e}")

            elif choice == "4":
                self.transaction_manager.list_transactions()
                try:
                    index = int(input("\nEnter transaction number to delete: ").strip())
                    confirm = (
                        input(
                            "⚠️ Are you sure you want to delete this transaction? (y/n): "
                        )
                        .strip()
                        .lower()
                    )
                    if confirm == "y":
                        self.transaction_manager.delete_transaction(index)
                    else:
                        print("❎ Deletion canceled.")
                except ValueError:
                    print("❌ Invalid input. Please enter a number.")
                except Exception as e:
                    print(f"Error deleting transaction: {e}")

            elif choice == "5":
                print(f"👋 Logging out {self.current_user.name}...")
                self.current_user = None
                break


def main():
    """Main entry point."""
    app = FinanceApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Exiting program.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

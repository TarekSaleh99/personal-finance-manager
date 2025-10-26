from modules.user_manager import UserManager
from modules.transaction_manager import TransactionManager
from modules.reports_manager import ReportsManager
import os


class FinanceApp:
    """Main application class for Personal Finance Manager."""

    def __init__(self):
        """Initialize the app with a UserManager."""
        self.user_manager = UserManager()
        self.current_user = None
        self.transaction_manager = None
        self.reports_manager = None

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
        print(f"\n===== {self.current_user.name}'s Dashboard =====")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Reports 📊")
        print("6. Logout")

        choice = input("Choose an option: ").strip()
        while choice not in ["1", "2", "3", "4", "5", "6"]:
            print("❌ Invalid choice. Please enter 1–6.")
            choice = input("Choose an option: ").strip()
        return choice

    # -------------------- REPORTS MENU --------------------
    def show_reports_menu(self):
        """Display the reports menu."""
        print("\n===== Reports Menu =====")
        print("1. Dashboard Summary")
        print("2. Monthly Report")
        print("3. Category Breakdown")
        print("4. Spending Trends")
        print("5. Back")

        choice = input("Choose a report: ").strip()
        while choice not in ["1", "2", "3", "4", "5"]:
            print("❌ Invalid choice. Please enter 1–5.")
            choice = input("Choose a report: ").strip()
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
                self.load_user_managers()
                self.transaction_loop()
        except Exception as e:
            print(f"Error during login: {e}")

    # -------------------- LOAD USER FILES --------------------
    def load_user_managers(self):
        """Load the transaction CSV and Reports manager for the logged-in user."""
        username = self.current_user.name
        user_id = self.current_user.user_id
        base_dir = "database"
        user_folder = f"{username}_{user_id[:8]}".replace(" ", "_")
        user_dir = os.path.join(base_dir, user_folder)
        csv_path = os.path.join(user_dir, "transactions.csv")

        self.transaction_manager = TransactionManager(csv_path)
        self.reports_manager = ReportsManager(user_dir)

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
                self.handle_reports_menu()

            elif choice == "6":
                print(f"👋 Logging out {self.current_user.name}...")
                self.current_user = None
                break

    # -------------------- REPORTS HANDLER --------------------
    def handle_reports_menu(self):
        """Handle all reports menu actions."""
        while True:
            choice = self.show_reports_menu()

            if choice == "1":
                self.reports_manager.dashboard_summary()
            elif choice == "2":
                try:
                    month = int(input("Enter month (1–12): "))
                    year = int(input("Enter year (e.g. 2025): "))
                    self.reports_manager.monthly_report(month, year)
                except ValueError:
                    print("❌ Please enter valid numbers for month and year.")
            elif choice == "3":
                self.reports_manager.category_breakdown()
            elif choice == "4":
                self.reports_manager.spending_trends()
            elif choice == "5":
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

from modules.user_manager import UserManager
from modules.transaction_manager import TransactionManager
from modules.dashboard_manager import Dashboard
import os


class FinanceApp:
    """Main application class for Personal Finance Manager."""

    def __init__(self):
        self.user_manager = UserManager()
        self.current_user = None
        self.transaction_manager = None
        self.dashboard = None

    # -------------------- MAIN MENU --------------------
    def show_main_menu(self):
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
        print("\n===== Dashboard & Transactions =====")
        print("1. View Dashboard/Profile")
        print("2. Add Transaction")
        print("3. View Transactions")
        print("4. Edit Transaction")
        print("5. Delete Transaction")
        print("6. Search Transactions")
        print("7. Filter Transactions")
        print("8. Logout")

        choice = input("Choose an option: ").strip()
        while choice not in [str(i) for i in range(1, 9)]:
            print("❌ Invalid choice. Please enter a number between 1–8.")
            choice = input("Choose an option: ").strip()
        return choice

    # -------------------- MAIN LOOP --------------------
    def run(self):
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
                self.load_user_data()
                self.dashboard.show_dashboard()  # Show dashboard immediately
                self.transaction_loop()
        except Exception as e:
            print(f"Error during login: {e}")

    # -------------------- LOAD USER DATA --------------------
    def load_user_data(self):
        username = self.current_user.name
        user_id = self.current_user.user_id
        base_dir = "database"
        user_folder = f"{username}_{user_id[:8]}".replace(" ", "_")
        csv_path = os.path.join(base_dir, user_folder, "transactions.csv")

        self.transaction_manager = TransactionManager(csv_path)
        self.dashboard = Dashboard(username, csv_path)

    # -------------------- TRANSACTION LOOP --------------------
    def transaction_loop(self):
        while True:
            choice = self.show_transaction_menu()

            if choice == "1":
                self.dashboard.show_dashboard()

            elif choice == "2":
                self.transaction_manager.add_transaction()

            elif choice == "3":
                self.transaction_manager.list_transactions()

            elif choice == "4":
                self.transaction_manager.list_transactions()
                try:
                    index = int(input("\nEnter transaction number to edit: ").strip())
                    self.transaction_manager.edit_transaction(index)
                except ValueError:
                    print("❌ Invalid input. Please enter a number.")
                except Exception as e:
                    print(f"Error editing transaction: {e}")

            elif choice == "5":
                self.transaction_manager.list_transactions()
                try:
                    index = int(input("\nEnter transaction number to delete: ").strip())
                    confirm = input("⚠️ Are you sure you want to delete this transaction? (y/n): ").strip().lower()
                    if confirm == "y":
                        self.transaction_manager.delete_transaction(index)
                    else:
                        print("❎ Deletion canceled.")
                except ValueError:
                    print("❌ Invalid input. Please enter a number.")
                except Exception as e:
                    print(f"Error deleting transaction: {e}")

            elif choice == "6":
                keyword = input("Enter keyword to search: ").strip()
                self.transaction_manager.search_transactions(keyword)

            elif choice == "7":
                print("\n--- Apply Filters ---")
                t_type = input("Type (Income/Expense or leave blank): ").strip()
                category = input("Category (or leave blank): ").strip()
                start_date = input("Start Date (YYYY-MM-DD or leave blank): ").strip()
                end_date = input("End Date (YYYY-MM-DD or leave blank): ").strip()
                min_amount = input("Min Amount (or leave blank): ").strip()
                max_amount = input("Max Amount (or leave blank): ").strip()
                payment_method = input("Payment Method (or leave blank): ").strip()

                self.transaction_manager.filter_transactions(
                    t_type or None,
                    category or None,
                    start_date or None,
                    end_date or None,
                    min_amount or None,
                    max_amount or None,
                    payment_method or None,
                )

            elif choice == "8":
                print(f"👋 Logging out {self.current_user.name}...")
                self.current_user = None
                break


def main():
    app = FinanceApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Exiting program.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

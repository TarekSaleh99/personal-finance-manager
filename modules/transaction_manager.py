import csv
import os
from datetime import datetime


class TransactionManager:
    """Handles all operations related to transactions for a user."""

    def __init__(self, user_csv_path):
        """
        Initialize the transaction manager with the user's CSV path.
        :param user_csv_path: Path to the user's transactions.csv file
        """
        self.user_csv_path = user_csv_path
        self.headers = [
            "Date",
            "Type",
            "Category",
            "Amount",
            "Payment Method",
            "Description",
        ]

        # Ensure file exists with headers
        if not os.path.exists(self.user_csv_path):
            with open(self.user_csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)

    # -------------------- VALIDATION HELPERS --------------------
    def _validate_date(self, date_str):
        """Validate date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _validate_amount(self, amount):
        """Check that amount is a positive number."""
        try:
            val = float(amount)
            return val >= 0
        except ValueError:
            return False

    def _validate_type(self, t_type):
        """Validate transaction type."""
        return t_type.lower() in ["income", "expense"]

    def _validate_payment_method(self, method):
        """Validate payment method."""
        allowed = ["cash", "card", "bank transfer", "wallet", "other"]
        return method.lower() in allowed

    # -------------------- ADD TRANSACTION --------------------
    def add_transaction(self):
        """Add a new transaction with input validation."""
        try:
            print("\n--- Add Transaction ---")

            # Date
            date_input = input(
                "Enter transaction date (YYYY-MM-DD) or leave blank for today: "
            ).strip()
            if not date_input:
                date_input = datetime.now().strftime("%Y-%m-%d")
            elif not self._validate_date(date_input):
                print("❌ Invalid date format. Use YYYY-MM-DD.")
                return

            # Type
            t_type = input("Enter type (Income/Expense): ").strip().lower()
            if not self._validate_type(t_type):
                print("❌ Invalid type. Please enter 'Income' or 'Expense'.")
                return
            t_type = t_type.capitalize()

            # Category
            category = (
                input("Enter category (e.g., Food, Rent, Salary): ")
                .strip()
                .capitalize()
            )
            if not category:
                print("❌ Category cannot be empty.")
                return

            # Amount
            amount = input("Enter amount: ").strip()
            if not self._validate_amount(amount):
                print("❌ Invalid amount. Please enter a valid number.")
                return

            # Payment Method
            payment_method = (
                input(
                    "Enter payment method (Cash, Card, Bank Transfer, Wallet, Other): "
                )
                .strip()
                .lower()
            )
            if not self._validate_payment_method(payment_method):
                print("❌ Invalid payment method.")
                return
            payment_method = payment_method.title()

            # Description (optional)
            description = input("Enter description (optional): ").strip()

            # Write to CSV
            with open(self.user_csv_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [date_input, t_type, category, amount, payment_method, description]
                )

            print("✅ Transaction added successfully.")

        except Exception as e:
            print(f"Error adding transaction: {e}")

    # -------------------- LIST TRANSACTIONS --------------------
    def list_transactions(self):
        """Display all transactions."""
        try:
            with open(self.user_csv_path, "r") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if not rows:
                    print("No transactions found.")
                    return

                print("\n--- Transactions ---")
                for i, row in enumerate(rows, start=1):
                    print(
                        f"{i}. {row['Date']} | {row['Type']} | {row['Category']} | "
                        f"{row['Amount']} | {row['Payment Method']} | {row['Description']}"
                    )
        except Exception as e:
            print(f"Error reading transactions: {e}")

    # -------------------- EDIT TRANSACTION --------------------
    def edit_transaction(self, index):
        """Edit an existing transaction by its index (1-based)."""
        try:
            with open(self.user_csv_path, "r", newline="") as f:
                reader = list(csv.DictReader(f))

            if index < 1 or index > len(reader):
                print("❌ Invalid transaction number.")
                return

            transaction = reader[index - 1]
            print("\n--- Editing Transaction ---")
            print(f"Current: {transaction}")

            # Input new values (skip empty)
            new_date = input(f"New Date (YYYY-MM-DD) [{transaction['Date']}]: ").strip()
            if new_date and not self._validate_date(new_date):
                print("❌ Invalid date format.")
                return
            if new_date:
                transaction["Date"] = new_date

            new_type = input(
                f"New Type (Income/Expense) [{transaction['Type']}]: "
            ).strip()
            if new_type:
                if not self._validate_type(new_type):
                    print("❌ Invalid type.")
                    return
                transaction["Type"] = new_type.capitalize()

            new_category = input(f"New Category [{transaction['Category']}]: ").strip()
            if new_category:
                transaction["Category"] = new_category.capitalize()

            new_amount = input(f"New Amount [{transaction['Amount']}]: ").strip()
            if new_amount:
                if not self._validate_amount(new_amount):
                    print("❌ Invalid amount.")
                    return
                transaction["Amount"] = new_amount

            new_method = input(
                f"New Payment Method [{transaction['Payment Method']}]: "
            ).strip()
            if new_method:
                if not self._validate_payment_method(new_method):
                    print("❌ Invalid payment method.")
                    return
                transaction["Payment Method"] = new_method.title()

            new_desc = input(
                f"New Description [{transaction['Description']}]: "
            ).strip()
            if new_desc:
                transaction["Description"] = new_desc

            # Save back to file
            with open(self.user_csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(reader)

            print("✅ Transaction updated successfully.")

        except Exception as e:
            print(f"Error editing transaction: {e}")

    # -------------------- DELETE TRANSACTION --------------------
    def delete_transaction(self, index):
        """Delete a transaction by its index (1-based)."""
        try:
            with open(self.user_csv_path, "r", newline="") as f:
                reader = list(csv.DictReader(f))

            if index < 1 or index > len(reader):
                print("❌ Invalid transaction number.")
                return

            deleted = reader.pop(index - 1)

            with open(self.user_csv_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(reader)

            print(
                f"✅ Deleted transaction: {deleted['Category']} ({deleted['Amount']})"
            )

        except Exception as e:
            print(f"Error deleting transaction: {e}")

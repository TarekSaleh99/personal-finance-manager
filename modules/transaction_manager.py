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
        self.headers = ["Date", "Type", "Category", "Amount"]

        # Ensure file exists
        if not os.path.exists(self.user_csv_path):
            with open(self.user_csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)

    # -------------------- ADD TRANSACTION --------------------
    def add_transaction(self, t_type, category, amount):
        """Add a new transaction."""
        try:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.user_csv_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([date, t_type, category, amount])
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
                        f"{i}. {row['Date']} | {row['Type']} | {row['Category']} | ${row['Amount']}"
                    )
        except Exception as e:
            print(f"Error reading transactions: {e}")

    # -------------------- EDIT TRANSACTION --------------------
    def edit_transaction(
        self, index, new_type=None, new_category=None, new_amount=None
    ):
        """Edit an existing transaction by its index (1-based)."""
        try:
            with open(self.user_csv_path, "r", newline="") as f:
                reader = list(csv.DictReader(f))

            if index < 1 or index > len(reader):
                print("Invalid transaction number.")
                return

            transaction = reader[index - 1]
            if new_type:
                transaction["Type"] = new_type
            if new_category:
                transaction["Category"] = new_category
            if new_amount:
                transaction["Amount"] = new_amount

            # Rewrite file
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
                print("Invalid transaction number.")
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

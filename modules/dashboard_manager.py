from decimal import Decimal
import csv
from datetime import datetime


class Dashboard:
    """Display a simple user dashboard/profile overview."""

    def __init__(self, username, user_csv_path):
        self.username = username
        self.user_csv_path = user_csv_path

    def _read_transactions(self):
        """Read all transactions from the user's CSV file."""
        try:
            with open(self.user_csv_path, "r") as f:
                return list(csv.DictReader(f))
        except Exception:
            return []

    def show_dashboard(self):
        """Display profile info, financial summary, and rent reminder."""
        rows = self._read_transactions()
        total_income = Decimal("0.00")
        total_expense = Decimal("0.00")
        rent_found = False

        # --- Calculate totals and check for Rent expense ---
        for row in rows:
            try:
                amount = Decimal(row["Amount"])
                t_type = row["Type"].strip().lower()
                category = row["Category"].strip().lower()

                if t_type == "income":
                    total_income += amount
                elif t_type == "expense":
                    total_expense += amount
                    if category == "rent":
                        rent_found = True
            except Exception:
                continue

        balance = total_income - total_expense

        # --- Display Dashboard ---
        print("\n📊 --- User Dashboard ---")
        print(f"👤 Username: {self.username}")
        print(f"📅 Joined On: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"🧾 Total Transactions: {len(rows)}")
        print(f"💰 Total Income:  +{total_income}")
        print(f"💸 Total Expense: -{total_expense}")
        print(f"💵 Net Balance:   {balance}")

        # --- Rent Reminder ---
        if rent_found:
            print("🏠 Reminder: You have a Rent expense recorded. Make sure it's paid on time!")

        print("-------------------------------")

        # --- Show last 3 transactions ---
        if rows:
            print("🕒 Recent Transactions:")
            for row in rows[-3:]:
                print(f"  {row['Date']} | {row['Type']} | {row['Category']} | {row['Amount']}")
        else:
            print("No transactions yet.")

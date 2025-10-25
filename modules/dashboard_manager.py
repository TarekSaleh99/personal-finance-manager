from decimal import Decimal
import csv
from datetime import datetime

class Dashboard:
    """Display a simple user dashboard/profile overview."""

    def __init__(self, username, user_csv_path):
        self.username = username
        self.user_csv_path = user_csv_path

    def _read_transactions(self):
        try:
            with open(self.user_csv_path, "r") as f:
                return list(csv.DictReader(f))
        except Exception:
            return []

    def show_dashboard(self):
        """Display profile info and financial summary."""
        rows = self._read_transactions()
        total_income = Decimal("0.00")
        total_expense = Decimal("0.00")

        for row in rows:
            try:
                amount = Decimal(row["Amount"])
                if row["Type"].lower() == "income":
                    total_income += amount
                elif row["Type"].lower() == "expense":
                    total_expense += amount
            except Exception:
                continue

        balance = total_income - total_expense

        print("\n📊 --- User Dashboard ---")
        print(f"👤 Username: {self.username}")
        print(f"📅 Joined On: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"🧾 Total Transactions: {len(rows)}")
        print(f"💰 Total Income:  +{total_income}")
        print(f"💸 Total Expense: -{total_expense}")
        print(f"💵 Net Balance:   {balance}")
        print("-------------------------------")

        # Show last 3 transactions
        if rows:
            print("🕒 Recent Transactions:")
            for row in rows[-3:]:
                print(f"  {row['Date']} | {row['Type']} | {row['Category']} | {row['Amount']}")
        else:
            print("No transactions yet.")

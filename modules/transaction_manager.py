import csv
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation


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
            val = Decimal(amount)
            return val >= 0
        except (InvalidOperation, ValueError):
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

    # -------------------- READ TRANSACTIONS --------------------
    def _read_transactions(self):
        try:
            with open(self.user_csv_path, "r") as f:
                return list(csv.DictReader(f))
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    # -------------------- LIST TRANSACTIONS --------------------
    def list_transactions(self):
        """Display all transactions."""
        rows = self._read_transactions()
        if not rows:
            print("No transactions found.")
            return

        print("\n--- Transactions ---")
        for i, row in enumerate(rows, start=1):
            print(
                f"{i}. {row['Date']} | {row['Type']} | {row['Category']} | "
                f"{row['Amount']} | {row['Payment Method']} | {row['Description']}"
            )

    # -------------------- BALANCE FEATURE --------------------
    def calculate_balance(self):
        """Calculate total income, total expenses, and net balance."""
        rows = self._read_transactions()
        income_total = Decimal("0.00")
        expense_total = Decimal("0.00")

        for row in rows:
            try:
                amount = Decimal(row["Amount"])
                if row["Type"].lower() == "income":
                    income_total += amount
                elif row["Type"].lower() == "expense":
                    expense_total += amount
            except (InvalidOperation, KeyError):
                continue

        balance = income_total - expense_total
        return income_total, expense_total, balance

    def view_balance(self):
        """Display current financial summary."""
        income_total, expense_total, balance = self.calculate_balance()

        print("\n💰 --- Balance Summary ---")
        print(f"Total Income:  +{income_total}")
        print(f"Total Expense: -{expense_total}")
        print(f"------------------------------")
        if balance >= 0:
            print(f"Net Balance:   ✅ {balance}")
        else:
            print(f"Net Balance:   🔴 {balance}")

    # -------------------- SEARCH TRANSACTIONS --------------------
    def search_transactions(self, keyword):
        """Search transactions by keyword in category, payment method, or description."""
        rows = self._read_transactions()
        keyword = keyword.lower()
        results = [
            row
            for row in rows
            if keyword in row["Category"].lower()
            or keyword in row["Payment Method"].lower()
            or keyword in row["Description"].lower()
        ]

        if results:
            print(f"\n🔎 Search Results for '{keyword}':")
            for i, row in enumerate(results, start=1):
                print(
                    f"{i}. {row['Date']} | {row['Type']} | {row['Category']} | "
                    f"{row['Amount']} | {row['Payment Method']} | {row['Description']}"
                )
        else:
            print(f"\n❌ No transactions found matching '{keyword}'.")

    # -------------------- FILTER TRANSACTIONS --------------------
    def filter_transactions(
        self,
        t_type=None,
        category=None,
        start_date=None,
        end_date=None,
        min_amount=None,
        max_amount=None,
        payment_method=None,
    ):
        """Filter transactions based on multiple criteria."""
        rows = self._read_transactions()

        def parse_date(d):
            return datetime.strptime(d, "%Y-%m-%d") if d else None

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        min_amount = Decimal(min_amount) if min_amount else None
        max_amount = Decimal(max_amount) if max_amount else None

        results = []
        for row in rows:
            try:
                row_date = parse_date(row["Date"])
                row_amount = Decimal(row["Amount"])

                if t_type and row["Type"].lower() != t_type.lower():
                    continue
                if category and row["Category"].lower() != category.lower():
                    continue
                if payment_method and row["Payment Method"].lower() != payment_method.lower():
                    continue
                if start_date and row_date < start_date:
                    continue
                if end_date and row_date > end_date:
                    continue
                if min_amount and row_amount < min_amount:
                    continue
                if max_amount and row_amount > max_amount:
                    continue

                results.append(row)
            except Exception:
                continue

        if results:
            print("\n✅ Filtered Transactions:")
            for i, row in enumerate(results, start=1):
                print(
                    f"{i}. {row['Date']} | {row['Type']} | {row['Category']} | "
                    f"{row['Amount']} | {row['Payment Method']} | {row['Description']}"
                )
        else:
            print("\n❌ No transactions match your filters.")

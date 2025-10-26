import pandas as pd
from datetime import datetime
import os
import csv


class ReportsManager:
    def __init__(self, user_dir):
        self.user_dir = user_dir
        self.csv_path = os.path.join(user_dir, "transactions.csv")
        self.export_dir = os.path.join(user_dir, "exports")
        os.makedirs(self.export_dir, exist_ok=True)

    # -------------------- EXPORT TO CSV --------------------
    def export_to_csv(self):
        """Export transactions to a new CSV file for backup or analysis."""
        if not os.path.exists(self.csv_path):
            print("❌ No transaction data found to export.")
            return

        export_file = os.path.join(self.export_dir, "transactions_export.csv")

        try:
            with (
                open(self.csv_path, "r", encoding="utf-8") as infile,
                open(export_file, "w", encoding="utf-8", newline="") as outfile,
            ):
                reader = csv.reader(infile)
                writer = csv.writer(outfile)
                for row in reader:
                    writer.writerow(row)

            print(f"✅ Transactions successfully exported to: {export_file}")
        except Exception as e:
            print(f"❌ Error exporting CSV: {e}")

    # -------------------- IMPORT FROM CSV --------------------
    def import_from_csv(self):
        """Import transactions from a CSV file (must match columns)."""
        file_path = input("Enter CSV file path to import: ").strip()
        if not os.path.exists(file_path):
            print("❌ File not found.")
            return

        try:
            with (
                open(file_path, "r", encoding="utf-8") as infile,
                open(self.csv_path, "a", encoding="utf-8", newline="") as outfile,
            ):
                reader = csv.reader(infile)
                writer = csv.writer(outfile)

                next(reader, None)  # Skip header if exists
                for row in reader:
                    writer.writerow(row)

            print(f"✅ Transactions imported successfully from: {file_path}")
        except Exception as e:
            print(f"❌ Error importing CSV: {e}")

    def load_data(self):
        try:
            return pd.read_csv(self.csv_path)
        except FileNotFoundError:
            print("No transactions found.")
            return pd.DataFrame()

    def dashboard_summary(self):
        df = self.load_data()
        if df.empty:
            print("No data available for summary.")
            return
        total_spent = df["Amount"].sum()
        total_transactions = len(df)
        avg_transaction = df["Amount"].mean()
        print(f"\n=== Dashboard Summary ===")
        print(f"Total Transactions: {total_transactions}")
        print(f"Total Spent: {total_spent:.2f}")
        print(f"Average Transaction: {avg_transaction:.2f}")

    def monthly_report(self, month, year):
        df = self.load_data()
        if df.empty:
            return
        df["Date"] = pd.to_datetime(df["Date"])
        monthly_df = df[(df["Date"].dt.month == month) & (df["Date"].dt.year == year)]
        print(f"\n=== Monthly Report ({month}/{year}) ===")
        print(monthly_df)

    def category_breakdown(self):
        df = self.load_data()
        if df.empty:
            return
        breakdown = df.groupby("Category")["Amount"].sum()
        print("\n=== Category Breakdown ===")
        print(breakdown)

    def spending_trends(self):
        df = self.load_data()
        if df.empty:
            return
        df["Date"] = pd.to_datetime(df["Date"])
        trends = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum()
        print("\n=== Spending Trends (Monthly) ===")
        print(trends)

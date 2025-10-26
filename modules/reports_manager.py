import pandas as pd
from datetime import datetime


class ReportsManager:
    def __init__(self, user_folder):
        self.csv_path = f"{user_folder}/transactions.csv"

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

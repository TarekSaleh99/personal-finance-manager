import json
import os
import csv

USERS_FILE = "users.json"
DATABASE_DIR = "database"


class DataHandler:
    def __init__(self):
        self.user_file = USERS_FILE
        self.database_dir = DATABASE_DIR
        try:
            self.ensure_files_exist()
        except Exception as e:
            print(f"Error initializing data handler: {e}")

    def ensure_files_exist(self):
        """Create files and directories if they don't exist"""
        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)
        if not os.path.exists(self.user_file):
            with open(self.user_file, "w") as f:
                json.dump({"users": []}, f, indent=4)

    def load_users(self):
        """Load users safely and recover from corruption"""
        try:
            with open(self.user_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("User file not found — creating a new one.")
            data = {"users": []}
            self.save_data(data)
        except json.JSONDecodeError:
            print("User file corrupted — recreating it.")
            data = {"users": []}
            self.save_data(data)
        return data

    def save_data(self, data):
        """Save users to JSON file"""
        try:
            with open(self.user_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def create_user_csv(self, user_id, username):
        """create a dedicated directory and csv file for the user."""
        try:
            safe_username = username.replace(" ", "_")
            user_folder = f"{safe_username}_{user_id[:8]}"
            user_dir = os.path.join(self.database_dir, user_folder)
            os.makedirs(user_dir, exist_ok=True)

            csv_filepath = os.path.join(user_dir, "transactions.csv")

            if not os.path.exists(csv_filepath):
                with open(csv_filepath, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        [
                            "Date",
                            "Type",
                            "Category",
                            "Amount",
                            "Payment Method",
                            "Description",
                        ]
                    )
                print(f"Created user data folder and CSV at: {csv_filepath}")
            else:
                print(f"CSV already exists for user: {csv_filepath}")
            return csv_filepath
        except Exception as e:
            print(f"Error createing user csv: {e}")
            return None

import json
import os

DATA_FILE = 'data.json'

def load_data():
    """
    Loads data from the JSON file.
    If the file does not exist yet, it creates a new one with empty lists.
    """
    if not os.path.exists(DATA_FILE):
       print("Data file not found. Creating a new one...")
       data = {"users": [], "transactions": []}
       save_data(data)
       return data
    
    with open(DATA_FILE, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("Data file is corrupted or empty. Resetting it...")
            data = {"users": [], "transactions": []}
            save_data(data)
    return data

def save_data(data):
    """
    Saves the given data (dictionary) into the JSON file.
    """
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
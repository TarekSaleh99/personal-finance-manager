import uuid
from getpass import getpass
from .utils import hash_password, verify_password
from .data_handler import save_data


def register_user(data):
    """Handles new user registration."""
    print("Register New User")
    name = input("Enter your name: ").strip()

    # Check if user already exists to prevent duplicates
    for user in data["users"]:
        if user["name"] == name:
            print("User already exists. Please choose a different name.")
            return
    
    password = getpass("Enter your password: ").strip()


    user = {
        "user_id": str(uuid.uuid4()),
        "name": name,
        "password": hash_password(password)
    }

    data["users"].append(user)

    save_data(data) # immediately save after registration
    print(f"User '{name}' registered successfully.")


def login_user(data):
    print("User Login")
    name = input("Enter your name: ").strip()
    password = getpass("Enter your password: ").strip()

    for user in data["users"]:
        if user["name"].lower() == name.lower() and verify_password(password,user["password"]):
            print(f"Welcome back, {name}")
            return user
    
    print("Invalid name or password.")
    return None
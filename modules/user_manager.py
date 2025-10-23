import uuid
from getpass import getpass
from .utils import PasswordHelper
from .data_handler import DataHandler


class User:
    """class to represent a user."""
    
    def __init__(self, user_id, name, password_hash):
        """Create a user with id, name, and hashed password."""
        self.user_id = user_id
        self.name = name
        self.password_hash = password_hash
    
    def to_dict(self):
        """Convert user to dictionary for saving."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password_hash
        }
    
    @staticmethod
    def from_dict(data):
        """Create a User object from a dictionary."""
        return User(
            user_id=data["user_id"],
            name=data["name"],
            password_hash=data["password"]
        )

class UserManager:
    """Class to manage user registration and login."""
    
    def __init__(self):
        """Initialize the UserManager with a DataHandler and PasswordHelper."""
        self.data_handler = DataHandler()
        self.password_helper = PasswordHelper()
    
    def register_user(self):
        """Handles new user registration."""
        try:
            data = self.data_handler.load_users()
        except Exception as e:
            print(f"Error loading users: {e}")
            return None
        
        print("Register New User")
        name = input("Enter your name: ").strip()
        if not name or not name.isalnum():
            print("Name must contain only letters or numbers.")
            return None
        
        # Check if user already exists to prevent duplicates
        for user_data in data["users"]:
            if user_data["name"].lower() == name.lower():
                print("User already exists. Please choose a different name.")
                return None
        
        password = getpass("Enter your password: ").strip()
        if not password or len(password) < 6 or " " in password:
            print("Password must be at least 6 characters and contain no spaces.")
            return None
        
        # Create new user
        try:
            user = User(
                user_id=str(uuid.uuid4()),
                name=name,
                password_hash=self.password_helper.hash_password(password)
            )
            
            # Add user to data and save
            data["users"].append(user.to_dict())
            self.data_handler.save_data(data)
        
            # Create personal CSV file for the user
            self.data_handler.create_user_csv(user.user_id, user.name)
        except Exception as e:
            print(f"Error during the registrations: {e}")
            return None
        
        print(f"User '{name}' registered successfully.")
        return user
    
    def login_user(self):
        """Handles user login."""
        try:
            data = self.data_handler.load_users()
        except Exception as e:
            print(f"Erro loading users: {e}")
            return None

        print("User Login")
        name = input("Enter your name: ").strip()
        password = getpass("Enter your password: ").strip()

        if not name or not password:
            print("Both name and password are required.")
            return None
        
        # Find and authenticate user
        try:
            for user_data in data["users"]:
                if user_data["name"].lower() == name.lower():
                    if self.password_helper.verify_password(password, user_data["password"]):
                        print(f"Welcome back, {name}")
                        return User.from_dict(user_data)
        except Exception as e:
            print(f"Error during login: {e}")
            return None
        
        print("Invalid name or password.")
        return None
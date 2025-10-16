from modules.user_manager import login_user, register_user
from modules.data_handler import load_data, save_data


def main_menu():
    """Display the main menu and return the user's choice."""
    print("Personal Finance Manager")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    return input("Choose an option: ").strip()

def main():
    """
    Main function to run the personal finance manager application.
    """
    data = load_data() # Load existing data or create new data file
    
    while True:
        choice = main_menu()

        if choice == '1':
            user = register_user(data) # Register a new user
            if user:
                print(f"You are now registered as {user['name']}.")
        elif choice == '2':
            user = login_user(data) # Log in an existing user
            if user:
                print(f"You are now logged in as {user['name']}.")
        elif choice == '3':
            save_data(data) # Save data before exiting
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
from modules.user_manager import UserManager


class FinanceApp:
    """Main application class for Personal Finance Manager."""
    
    def __init__(self):
        """Initialize the app with a UserManager."""
        self.user_manager = UserManager()
        self.current_user = None
    
    def show_menu(self):
        """Display the main menu and return the user's choice."""
        print("\nPersonal Finance Manager")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        return input("Choose an option: ").strip()
    
    def run(self):
        """Run the main application loop."""
        while True:
            choice = self.show_menu()
        
            if choice == '1':
                try:
                    user = self.user_manager.register_user()
                    if user:
                        print(f"You are now registered as {user.name}.")
                except Exception:
                    print(f"Error during registeration")
            
            elif choice == '2':
                try:
                    user = self.user_manager.login_user()
                    if user:
                        self.current_user = user
                        print(f"You are now logged in as {user.name}.")
                except Exception:
                    print(f"Erorr during login")
            
            elif choice == '3':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")


def main():
    """
    Main function to run the personal finance manager application.
    """
    app = FinanceApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting program.")
    except Exception:
        print("Unexpected Error ")


if __name__ == "__main__":
    main()
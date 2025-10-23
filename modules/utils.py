import hashlib


class PasswordHelper:
    """Simple class to handle password operations."""
    
    @staticmethod
    def hash_password(password):
        """Converts a password into its SHA-256 hash."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed):
        """Check if the provided password matches the hashed password."""
        return PasswordHelper.hash_password(password) == hashed
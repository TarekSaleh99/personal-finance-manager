import hashlib

def hash_password(password):
    """Converts a password into its SHA-256 hash."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    """Check if the provided password matches the hashed password."""
    return hash_password(password) == hashed
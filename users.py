import hashlib

# Simple user database (can be extended)
users = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "debrik": hashlib.sha256("doglover".encode()).hexdigest()
}

def authenticate(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return users.get(username) == hashed

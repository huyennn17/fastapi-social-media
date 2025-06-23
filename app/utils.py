from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash."""
    return pwd_context.verify(password, hashed)
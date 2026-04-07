from cryptography.fernet import Fernet
import os
from passlib.context import CryptContext

# Password hashing configuration (For User Login)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret Key for Data Encryption (Isse .env mein hona chahiye)
# Generate one using: Fernet.generate_key()
SECRET_KEY = b'PK8tQUPphL2PrXm-cMtCikEDxjuUfDBpYlvOr7XQpCI=' 
cipher_suite = Fernet(SECRET_KEY)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def encrypt_db_password(password: str) -> str:
    """SQL Server ka password encrypt karne ke liye"""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_db_password(encrypted_password: str) -> str:
    """Migration ke waqt password wapas nikalne ke liye"""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
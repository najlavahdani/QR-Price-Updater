import os
from src.db.database_manager import DatabaseManager
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_TEST_DIR= os.path.join(os.path.join(os.path.join(BASE_DIR, "assets"), "qrcodes"), "test")
os.makedirs(QR_TEST_DIR, exist_ok=True)

def setup_temp_db():
    db = DatabaseManager("sqlite:///:memory:")
    return db


from src.db.database_manager import DatabaseManager

def setup_temp_session():
    db=DatabaseManager("sqlite:///:memory:")
    return db.Session()

from src.db.database_manager import DatabaseManager


def setup_temp_db():
    #creating temporary database 
    db = DatabaseManager("sqlite:///:memory:")
    return db
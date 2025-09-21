import os
from sqlalchemy import create_engine
from src.db.models import Base

# project root path
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# data directory for DB
DATA_DIR= os.path.join(BASE_DIR, "data")
# the database path
DB_PATH= os.path.join(DATA_DIR, "app.db")
# the path where the DB should be created by sqlAlchemy
DB_URL= f"sqlite:///{DB_PATH}"

os.makedirs(DATA_DIR, exist_ok=True)

#creating the DB and tables
def init_db():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    print(f"Database created at {DB_PATH}")
    
    
if __name__ == "__main__":
    init_db()
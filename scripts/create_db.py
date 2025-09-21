import os

# project root path
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# data directory for DB
DATA_DIR= os.path.join(BASE_DIR, "data")
# the database path
DB_PATH= os.path.join(DATA_DIR, "app.db")
# the path where the DB should be created by sqlAlchemy
DB_URL= f"sqlite:///{DB_PATH}"

os.makedirs(DATA_DIR, exist_ok=True)
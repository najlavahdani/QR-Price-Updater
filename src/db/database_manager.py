import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base
 

BASE_DIR= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR= os.path.join(BASE_DIR, "data")
DB_PATH= os.path.join(DATA_DIR, "app.db")
DB_URL= f"sqlite:///{DB_PATH}"


class DatabaseManager:
    def __init__(self, db_url: str = DB_URL):
        self.engine = create_engine(db_url, echo= False, future= True)
        #creating tables if not exists
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind= self.engine, autiflush=False, future=True)
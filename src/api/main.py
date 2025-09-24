from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from src.db.database_manager import DatabaseManager
from src.services.exchange_rate import ExchangeRate
#project and template path
PROJECT_ROOT=  Path(__file__).resolve().parents[2]
templates= Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

app = FastAPI()

db= DatabaseManager(f"sqlite:///{PROJECT_ROOT}/data/app.db")

#dependency for Session
def get_session():
    with db.Session() as session:
        yield session
        
 
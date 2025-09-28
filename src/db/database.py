from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session as SessionType
from typing import Generator
#paths
BASE_DIR= Path(__file__).resolve().parents[1] #src/
DATA_DIR= BASE_DIR/"data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

DB_URL =f"sqlite:///{DB_PATH}"

connect_args= {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

#engin and session factory
engine= create_engine(DB_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal= sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)

Base = declarative_base()

def init_db() -> None:
    """
        Generate tables based on models.
        Caution: This built-in function imports models so that the model classes are registered on Base.
    """
    import src.db.models
    Base.metadata.create_all(bind=engine)
    
def get_engine():
    return engine

def get_session() -> Generator[SessionType, None, None]:
    """
        Dependency for FastAPI or anywhere else.
        Use in route: session: Session = Depends(get_session)
    """
    with SessionLocal() as session:
        yield session
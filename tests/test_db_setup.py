import pytest
from sqlalchemy import create_engine
from src.db.database import Base
from sqlalchemy.orm import sessionmaker
from src.db.database import get_session
from sqlalchemy import inspect

@pytest.fixture
def temp_engine():
    engine=create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()
    
@pytest.fixture
def temp_session(temp_engine):
    Session = sessionmaker(bind=temp_engine, autoflush=False, future=True)
    session= Session()
    yield session
    session.close()
    
def test_get_session(temp_session): #creating in-memory temp db and session
    with get_session() as session:
        #this command does not require any tables, it is only used to test the connection and correct db performance
        result = session.Execute("SELECT 1").scaler()
        assert result == 1
    
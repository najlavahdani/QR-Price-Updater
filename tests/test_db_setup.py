import pytest
from sqlalchemy import create_engine
from src.db.database import Base
from sqlalchemy.orm import sessionmaker

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
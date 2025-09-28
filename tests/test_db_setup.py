import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import get_session, init_db, Base
from sqlalchemy import inspect
from src.db.models import Settings
from src.db.init_db import seed_settings
from decimal import Decimal

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
        result = session.execute("SELECT 1").scalar()
        assert result == 1
    
def test_init_db_creates_tables(temp_engine):
    # Test that init_db creates tables into temp db
    init_db(engine_arg=temp_engine)
    
    #check that the tables has been created
    inspector = inspect(temp_engine)
    tables=inspector.get_table_names()
    assert "products" in tables
    assert "settings" in tables    
    
def test_seed_settings(temp_session):
    seed_settings(session_arg=temp_session)
    #the table is empty, adding seed
    row= temp_session.query(Settings).first()
    assert row is not None
    assert row.id == 1
    assert row.exchange_rate == Decimal("-1")    
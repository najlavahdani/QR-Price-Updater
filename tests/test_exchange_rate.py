import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import init_db
from src.services.exchange_rate import ExchangeRate
from decimal import Decimal

#----------fixtures----------
@pytest.fixture
def temp_session():
    #Creating a session on a temporary database in memory
    engine = create_engine("sqlite:///:memory:", future=True)
    init_db(engine_arg=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
    session = SessionLocal()
    yield session
    session.close()
    engine.dispose()
    
#----------text----------
def test_set_and_get_rate(temp_session):
    ex_rate= ExchangeRate(temp_session)
    
    ex_rate.set_rate(Decimal("100000"))
    rate= ex_rate.get_rate()
    
    assert rate == Decimal("100000")

    
def test_update_rate(temp_session):
    ex_rate= ExchangeRate(temp_session)
    
    ex_rate.set_rate(Decimal("60000"))
    ex_rate.set_rate(Decimal("65000"))  #update
    
    rate= ex_rate.get_rate()
    assert rate == Decimal("65000")
    

def test_calculate_price(temp_session):
    ex_rate = ExchangeRate(temp_session)
    
    ex_rate.set_rate(Decimal("60000"))
    result= ex_rate.calculate_price(Decimal("2"))
    
    assert Decimal(120000) == result
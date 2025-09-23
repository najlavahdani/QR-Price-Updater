from src.db.database_manager import DatabaseManager
from src.services.exchange_rate import ExchangeRate
from decimal import Decimal

def setup_temp_session():
    db=DatabaseManager("sqlite:///:memory:")
    return db.Session()


def test_set_and_get_rate():
    session= setup_temp_session()
    ex_rate= ExchangeRate(session)
    
    ex_rate.set_rate("USD", Decimal("100000"))
    rate= ex_rate.get_rate("USD")
    
    assert rate == Decimal("100000")

    
def test_update_rate():
    session= setup_temp_session()
    ex_rate= ExchangeRate(session)
    
    ex_rate.set_rate("USD", Decimal("60000"))
    ex_rate.set_rate("USD", Decimal("65000"))  #update
    
    rate= ex_rate.get_rate("USD")
    assert rate == Decimal("65000")
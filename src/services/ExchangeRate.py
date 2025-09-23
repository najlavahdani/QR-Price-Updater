from sqlalchemy.orm import Session
from decimal import Decimal
from src.db.models import Settings
class ExchangeRate:
    def __init__(self, session: Session):
        self.session = session
        
    
    def set_rate(self, currency: str, rate: Decimal):
        #add or update if already exists
        setting= self.session.query(Settings).filter_by(currency=currency).first()
        if setting: #true if the currency already exists
            setting.exchange_rate = rate
        else:
            setting= Settings(currency=currency, exchange_rate=rate)
            self.session.add(setting)
        self.session.commit()
        return setting #return the updated or new exchange setting
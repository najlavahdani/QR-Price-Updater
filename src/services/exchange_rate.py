from sqlalchemy.orm import Session
from decimal import Decimal
from src.db.models import Settings
from src.db.database import get_session

class ExchangeRate:
    def __init__(self, session: Session|None=None):
        #If session is not given, get_session is used in each method.
        self.external_session = session
        
    
    def set_rate(self, rate: Decimal):
        #If we have an external session, we use that, otherwise get_session opens and closes itself.
        if self.external_session:
            s= self.external_session
            setting = s.query(Settings).first() #get first record
                
            if setting: #true if first record exist
                setting.exchange_rate = rate
            else:
                setting= Settings(currency="DEFAULT", exchange_rate=rate)
                s.add(setting)
            s.commit()
            return setting #return the updated or new exchange setting
        else:
            with get_session() as s:
                setting = s.query(Settings).first()
                if setting:
                    setting.exchange_rate = rate
                else:
                    setting = Settings(currency= "DEFAULT", exchange_rate=rate) 
                    s.add(setting)
                s.commit()
                return setting
    
    def get_rate(self) -> Decimal:
        #Returns the exchange rate value of the first Settings record.
        if self.external_session:
            s=self.external_session
            setting=s.query(Settings).first()
        else:
            with get_session() as s:
                setting= s.query(Settings).first()
        if setting:
            return setting.exchange_rate
        raise ValueError("No exchange rate set.")        
                
    def calculate_price(self, usd_price: Decimal) -> Decimal:
        rate= self.get_rate()
        return usd_price*rate
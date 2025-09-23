from sqlalchemy.orm import Session

class ExchangeRate:
    def __init__(self, session: Session):
        self.session = session
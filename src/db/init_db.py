from src.db.database import get_session, init_db
from src.db.models import Settings
from decimal import Decimal
from sqlalchemy.orm import Session

def seed_settings(session_arg: Session=None):
    """
        it only adds a default row that exchange_rate=-1 in the settings table if the table is empty,
        after that, no changes to exchange_rate will be applied
    """
    if session_arg is not None:
        session= session_arg
        exists = session.query(Settings).first()
        if not exists:
            default_setting = Settings(
                id=1,
                currency = "USD",
                exchange_rate= Decimal("-1")                
            )
            session.add(default_setting)
            session.commit()
            print("Settings table seeded with default row.")
        else:
            print("Settings table already has data. Skipping seeding.")

    else:
        with get_session() as session:
            exists = session.query(Settings).first()
            if not exists:
                default_setting = Settings(
                    id=1,
                    currency = "USD",
                    exchange_rate= Decimal("-1")                
                )
                session.add(default_setting)
                session.commit()
                print("Settings table seeded with default row.")
            else:
                print("Settings table already has data. Skipping seeding.")

def main():
    #creating tables if if they don's exist
    init_db()
    
    #add default settings row only if Settings table is empty
    seed_settings()
    
if __name__ == "__main__":
    main()
import os
from typing import List, Dict
from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from src.db.models import Base, Products
 

BASE_DIR= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR= os.path.join(BASE_DIR, "data")
DB_PATH= os.path.join(DATA_DIR, "app.db")
DB_URL= f"sqlite:///{DB_PATH}"


class DatabaseManager:
    def __init__(self, db_url: str = DB_URL):
        self.engine = create_engine(db_url, echo= False, future= True)
        #creating tables if not exists
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind= self.engine, autiflush=False, future=True)
        
        
    def insert_or_update_products(self, products: List[Dict]) -> List[Dict]:
        """
        products: list of dicts with keys ProductID, Name, PriceUSD
        Returns list of result dicts: {'product_id': ..., 'action': 'inserted'|'updated'|'skipped', 'reason': ...}
        """
        results= []
        with self.Session() as session:
            try: 
                for p in products:
                    pid= str(p.get("ProductID")).strip()
                    name= str(p.get("Name")).strip
                    try:
                        price = Decimal(str(p.get("PriceUSD")))
                    except Exception:
                        results.append({"product_id": pid, "action": "skipped", "reason": "invalid PriceUSD"})
                        continue
                    
                    #ProductID shouldn't be null
                    if not pid:
                        results.append({"product_id": None, "action": "skipped", "reason": "empty ProductID"})
                        continue
                    
                    #check if the current product is already exists in DB or not: None if doesn't exists| Products object if exists
                    existing = session.query(Products).filter_by(product_id=pid).one_or_none()
                    if existing: #True if the current product already exists in DB
                        # the product will update only if there is a difference
                        changed= False
                        if existing.name != name:
                            existing.name = name
                            changed= True
                        if Decimal(str((existing.price))) != price:
                            existing.price = price
                            changed= True
                        
                        if changed: #True if update the product 
                            results.append({"product_id": pid, "action": "updated"})
                        else:
                            results.append({"product_id": pid, "action": "skipped", "reason": "already exist, with no changes"})
                            
                    else: #new product
                        new= Products(product_id=pid, name=name, price=price, qr_path=None)
                        session.add(new)
                        results.append({"product_id": pid, "action": "inserted"})
                session.commit()
            except Exception as exc:
                session.rollback()
                raise
        return results
    
    
    def get_all_products(self):
        with self.Session() as session:
            return session.query(Products).all()
        
    def get_product_by_id(self, product_id: str):
        with self.Session() as session:
            return session.query(Products).filter_by(product_id=product_id).one_or_none()
        
    def get_product_by_name(self, name: str):
        #fetch all products whose names contain text (case insensetive)
        with self.Session() as session:
            statement= select(Products).where(Products.name.ilike(f"%{name}%"))
            result= session.execute(statement).scalars().all()
            return result
from typing import List, Dict
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db.database import get_session
from src.db.models import Products
from src.services.qrcode_generator import QRCodeGenerator


class DatabaseManager:
    def __init__(self, qr_base_url: str = "http://example.com"):
        # create QR generator object (storage path is managed internally)
        self.qr_generator= QRCodeGenerator(qr_base_url)
        
    def insert_or_update_products(self, products: List[Dict], qrcode_generator: QRCodeGenerator=None) -> List[Dict]:
        """
        products: list of dicts with keys ProductID, Name, PriceUSD
        Returns list of result dicts: {'product_id': ..., 'action': 'inserted'|'updated'|'skipped', 'reason': ...}
        """
        results= []
        with self.Session() as session:
            try: 
                for p in products:
                    pid= str(p.get("ProductID")).strip()
                    name= str(p.get("Name")).strip()
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
                        new_product= Products(product_id=pid, name=name, price=price, qr_path=None)
                        session.add(new_product)
                        session.flush() #temporary commit to get id
                        
                        if qrcode_generator:
                            #generate qr with costum generator
                            qr_file_path=qrcode_generator.generate_qr(pid)
                            new_product.qr_path = qr_file_path
                        else:
                            #generating qr code with self.qr_generator
                            qr_file_path = self.qr_generator.generate_qr(pid)
                            new_product.qr_path = qr_file_path
                        
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
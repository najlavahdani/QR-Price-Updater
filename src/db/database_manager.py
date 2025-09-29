from typing import List, Dict
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db.database import get_session
from src.db.models import Products
from src.services.qrcode_generator import QRCodeGenerator
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, qr_base_url: str = "http://example.com"):
        # create QR generator object (storage path is managed internally)
        self.qr_generator= QRCodeGenerator(qr_base_url)
        
    def insert_or_update_products(self, products: List[Dict], qrcode_generator:QRCodeGenerator=None, session:Session|None=None) -> List[Dict]:
        """
        products: list of dicts with keys ProductID, Name, PriceUSD
        Returns list of result dicts: {'product_id': ..., 'action': 'inserted'|'updated'|'skipped', 'reason': ...}
        """
        results= []
        with get_session(session) as s:
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
                    existing = s.query(Products).filter_by(product_id=pid).one_or_none()
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
                        s.add(new_product)
                        s.flush() #temporary commit to get id
                        qr_gen_to_use= qrcode_generator or self.qr_generator
                        new_product.qr_path= qr_gen_to_use.generate_qr(pid)
                        results.append({"product_id": pid, "action": "inserted"})
                s.commit()
            except Exception as e:
                s.rollback()
                raise RuntimeError(f"DB insert faild: {e}")
        return results
    
    def insert_single_product(self, product: dict, **kwargs) -> dict:
        return self.insert_or_update_products([product], **kwargs)[0]
    
    def get_all_products(self, session: Session | None = None) -> List[Products]:
        with get_session(session) as s:
            return s.query(Products).all()
        
    def get_product_by_id(self, product_id: str, session: Session|None) -> Products | None:
        with get_session(session) as s:
            return s.query(Products).filter_by(product_id=product_id).one_or_none()
        
    def get_product_by_name(self, name: str, session: Session|None) -> List[Products]:
        #fetch all products whose names contain text (case insensetive)
        with get_session(session) as s:
            statement= select(Products).where(Products.name.ilike(f"%{name}%"))
            result= s.execute(statement).scalars().all()
            return result
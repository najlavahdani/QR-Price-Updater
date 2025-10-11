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
        own_session = False  # Track if we created the session ourselves

        if session is None:
            own_session = True
            session = get_session().__enter__()  # Manually enter context

        try:
            for p in products:
                pid = str(p.get("ProductID")).strip()
                name = str(p.get("Name")).strip()

                try:
                    price = Decimal(str(p.get("PriceUSD")))
                except Exception:
                    results.append({"product_id": pid, "action": "skipped", "reason": "invalid PriceUSD"})
                    continue

                if not pid:
                    results.append({"product_id": None, "action": "skipped", "reason": "empty ProductID"})
                    continue

                existing = session.query(Products).filter_by(product_id=pid).one_or_none()
                if existing:
                    changed = False
                    if existing.name != name:
                        existing.name = name
                        changed = True
                    if Decimal(str(existing.price)) != price:
                        existing.price = price
                        changed = True

                    if changed:
                        results.append({"product_id": pid, "action": "updated"})
                    else:
                        results.append({"product_id": pid, "action": "skipped", "reason": "already exist, with no changes"})
                else:
                    new_product = Products(product_id=pid, name=name, price=price, qr_path=None)
                    session.add(new_product)
                    session.flush()

                    qr_gen_to_use = qrcode_generator or self.qr_generator
                    new_product.qr_path = qr_gen_to_use.generate_qr(pid)
                    results.append({"product_id": pid, "action": "inserted"})

            session.commit()
        except Exception as e:
            session.rollback()
            raise RuntimeError(f"DB insert failed: {e}")
        finally:
            if own_session:
                session.__exit__(None, None, None)

        return results
    
    def insert_single_product(self, product: dict, *args, session: Session | None = None, **kwargs) -> dict:
        return self.insert_or_update_products([product], *args, session=session, **kwargs)[0]
    
    def get_all_products(self, session: Session | None = None) -> List[Products]:
        own_session = False
        if session is None:
            own_session = True
            session = get_session().__enter__()
        try:
            return session.query(Products).all()
        finally:
            if own_session:
                session.__exit__(None, None, None)
        
    def get_product_by_id(self, product_id: str, session: Session|None) -> Products | None:
        with get_session() as s:
            return s.query(Products).filter_by(product_id=product_id).one_or_none()
        
    def get_product_by_name(self, name: str, session: Session|None) -> List[Products]:
        #fetch all products whose names contain text (case insensetive)
        with get_session() as s:
            statement= select(Products).where(Products.name.ilike(f"%{name}%"))
            result= s.execute(statement).scalars().all()
            return result
        
    def delete_product(self, product_id: str):
        """
        Delete a product from the database by its ProductID.
        """
        own_session = False
        if session is None:
            own_session = True
            session = get_session().__enter__()
        try:
            product = session.query(Products).filter_by(product_id=product_id).first()
            if not product:
                raise ValueError(f"Product with ID {product_id} not found.")
            session.delete(product)
            session.commit()
            return {"status": "deleted", "product_id": product_id}
        finally:
            if own_session:
                session.__exit__(None, None, None)
        
        

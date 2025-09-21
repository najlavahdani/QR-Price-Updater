from sqlalchemy import Column, Integer, String, Float, Numeric
from sqlalchemy.orm import declarative_base

Base= declarative_base() 


#products table
class Products(Base):
    __tablename__ = "products"

    id= Column(Integer, primary_key=True, autoincrement=True)
    product_id= Column(String, unique=True, nullable=False)
    name= Column(String, nullable=False)
    price= Column(Float, nullable=False)
    qr_path= Column(String, nullable=True)
    
    


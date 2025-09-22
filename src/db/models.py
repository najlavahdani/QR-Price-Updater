from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base

Base= declarative_base() 


#products table
class Products(Base):
    __tablename__ = "products"

    id= Column(Integer, primary_key=True, autoincrement=True)
    product_id= Column(String, unique=True, nullable=False)
    name= Column(String, nullable=False)
    price= Column(Numeric(10,2), nullable=False)
    qr_path= Column(String, nullable=True)
    
    

# general settings table
class Settings(Base):
    __tablename__ = "settings"
    
    id= Column(Integer, primary_key=True, autoincrement=True)
    currency= Column(String, unique=True, nullable=False)
    exchange_rate= Column(Numeric(10,2), nullable=False)
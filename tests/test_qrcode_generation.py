import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.database import init_db
from src.db.database_manager import DatabaseManager
from src.services.qrcode_generator import QRCodeGenerator

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_TEST_DIR= os.path.join(os.path.join(os.path.join(BASE_DIR, "assets"), "qrcodes"), "qr_gen_test")
os.makedirs(QR_TEST_DIR, exist_ok=True)


#----------fixtures----------
@pytest.fixture 
def temp_engine():
    #temp in-memory db
    engine= create_engine("sqlite:///:memory:", future= True)
    init_db(engine_arg=engine)
    yield engine
    engine.dispose()
    

@pytest.fixture
def temp_session(temp_engine):
    SessionLocal= sessionmaker(bind=temp_engine, autoflush=False, expire_on_commit=False, future=True)
    session= SessionLocal()
    yield session
    session.close()
    

@pytest.fixture
def db_manager(temp_session):
    dbm= DatabaseManager()
    return dbm, temp_session


#----------tests----------
def test_insert_and_update_products_with_custom_qr(db_manager):
    db, session= db_manager
    
    #custom qr generator
    qr_gen= QRCodeGenerator(base_url="http://example.com", png_files_dir=QR_TEST_DIR)

    #new products
    products= [
        {"ProductID": "P900", "Name": "Test Product 1", "PriceUSD": "10.00"},
        {"ProductID": "P901", "Name": "Test Product 2", "PriceUSD": "20.50"},
    ]
    
    #test inserting products with qr codes
    insertion_result = db.insert_or_update_products(products, qr_gen, session=session)
    assert insertion_result[0]["action"] == "inserted"
    assert insertion_result[1]["action"] == "inserted"
    
    #checking products qr codes paths
    for p in products:
        prod= db.get_product_by_id(p["ProductID"], session=session)
        assert prod.qr_path is not None
        assert os.path.exists(prod.qr_path)
        assert prod.qr_path.startswith(QR_TEST_DIR)
        print(f"QR for {p['ProductID']} generated at: {prod.qr_path}")
        
    qr_path_before_update= db.get_product_by_id("P900", session=session).qr_path 
    
    #product update without changing QR
    updated_product=  {"ProductID": "P900", "Name": "Test Product 1 Updated", "PriceUSD": "12.00"}
    updating_result= db.insert_or_update_products([updated_product], qr_gen, session=session)
    assert updating_result[0]["action"] == "updated"
    
    #checking that the QR code has not been changed
    prod_after_update= db.get_product_by_id("P900", session=session)
    qr_path_after_update = db.get_product_by_id("P900", session=session).qr_path
    assert qr_path_before_update == qr_path_after_update
    print(f"QR path after update remains: {prod_after_update.qr_path}")
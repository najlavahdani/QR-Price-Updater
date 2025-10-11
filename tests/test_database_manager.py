import pytest
from src.db.database_manager import DatabaseManager
from src.db.models import Products
from sqlalchemy.orm import sessionmaker
from src.db.database import init_db
from decimal import Decimal
from sqlalchemy import create_engine
import os
from src.services.qrcode_generator import QRCodeGenerator

#custom path to save qr images
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_TEST_DIR_IN_DBMANG= os.path.join(os.path.join(os.path.join(BASE_DIR, "assets"), "qrcodes"), "db_mang_test")
os.makedirs(QR_TEST_DIR_IN_DBMANG, exist_ok=True)

#custom qr generator
qr_gen= QRCodeGenerator(base_url="http://example.com", png_files_dir=QR_TEST_DIR_IN_DBMANG)

#----------fixtures----------
@pytest.fixture
def temp_session():
    #Create an in-memory SQLite database and return a temporary session
    engine = create_engine("sqlite:///:memory:", future=True)
    init_db(engine_arg=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False,
                                expire_on_commit=False, future=True)
    session = SessionLocal()
    yield session
    session.close()
    engine.dispose()
    
@pytest.fixture
def db_manager():
    #DatabaseManager without default Session (session is passed in tests)
    return DatabaseManager()

#----------Tests----------
def test_insert_update_product(db_manager, temp_session, qr_gen):
    # cleaning database
    temp_session.query(Products).delete()
    temp_session.commit()

    #insert test
    products = [
        {"ProductID": "P200", "Name": "Laptop Dell", "PriceUSD": "1000.50"},
        {"ProductID": "P201", "Name": "Laptop HP", "PriceUSD": "950.75"},
    ]

    result = db_manager.insert_or_update_products(products, qr_gen)
    assert result[0]["action"] == "inserted"
    assert result[1]["action"] == "inserted"

    
    with db_manager.get_session() as s:
        p200 = s.query(Products).filter_by(product_id="P200").one()
        p201 = s.query(Products).filter_by(product_id="P201").one()
        assert p200.name == "Laptop Dell"
        assert p201.price == Decimal("950.75")

    #update test
    prod_to_update = {"ProductID": "P200", "Name": "Laptop Dell X", "PriceUSD": "1100.00"}
    update_result = db_manager.insert_or_update_products([prod_to_update], qr_gen)
    assert update_result[0]["action"] == "updated"

    
    with db_manager.get_session() as s:
        updated_prod = s.query(Products).filter_by(product_id="P200").one()
        assert updated_prod.name == "Laptop Dell X"
        assert updated_prod.price == Decimal("1100.00")

    #skip test
    prod_no_change = {"ProductID": "P201", "Name": "Laptop HP", "PriceUSD": "950.75"}
    no_change_result = db_manager.insert_or_update_products([prod_no_change], qr_gen)
    assert no_change_result[0]["action"] == "skipped"
    assert "no changes" in no_change_result[0]["reason"]    

def teat_insert_single_product(db_manager, temp_session):
    #single product
    product= {"ProductID": "P500", "Name": "Webcam Logitech", "PriceUSD": "75.50"}
    
    #insert only 1 product
    result= db_manager.insert_single_product(product, qr_gen, session=temp_session)
    
    #result check
    assert result["action"] == "inserted"
    assert result["product_id"] == "P500"

    #database check
    prod_in_db= db_manager.get_product_by_id("P500", session=temp_session)
    assert prod_in_db is not None
    assert prod_in_db.name == "Webcam Logitech"
    assert prod_in_db.price == Decimal("75.50")
    assert prod_in_db.qr_path ==  os.path.join(QR_TEST_DIR_IN_DBMANG, "P500.png")

def test_get_product_by_id(db_manager, temp_session):
    product = {"ProductID": "P200", "Name": "Mouse Logitech", "PriceUSD": "25.99"}
    db_manager.insert_or_update_products([product], qr_gen, session=temp_session)
    
    retrieved_prod = db_manager.get_product_by_id("P200",session=temp_session)
    assert retrieved_prod is not None
    assert retrieved_prod.name == "Mouse Logitech"
    assert retrieved_prod.price == Decimal("25.99")


def test_get_products_by_name(db_manager, temp_session):
    products = [
        {"ProductID": "P300", "Name": "Keyboard Logitech", "PriceUSD": "45.00"},
        {"ProductID": "P301", "Name": "Keyboard Dell", "PriceUSD": "55.00"},
        {"ProductID": "P302", "Name": "Monitor LG", "PriceUSD": "150.00"},
    ]
    
    db_manager.insert_or_update_products(products, qr_gen, session=temp_session)
    
    keyboards = db_manager.get_product_by_name("Keyboard", session=temp_session)
    assert len(keyboards) == 2
    ids = [p.product_id for p in keyboards]
    assert "P300" in ids
    assert "P301" in ids
    
    
def test_get_all_products(db_manager, temp_session):
    products = [
        {"ProductID": "P400", "Name": "Tablet Samsung", "PriceUSD": "300.00"},
        {"ProductID": "P401", "Name": "Tablet Apple", "PriceUSD": "800.00"},
    ]
    db_manager.insert_or_update_products(products, qr_gen, session=temp_session)
    
    all_products = db_manager.get_all_products(session=temp_session)
    ids = [p.product_id for p in all_products]
    assert "P401" in ids
    assert "P400" in ids
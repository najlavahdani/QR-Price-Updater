from src.db.database_manager import DatabaseManager
from decimal import Decimal
import os
from src.services.qrcode_generator import QRCodeGenerator

#custom path to save qr images
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_TEST_DIR_IN_DBMANG= os.path.join(os.path.join(os.path.join(BASE_DIR, "assets"), "qrcodes"), "db_mang_test")
os.makedirs(QR_TEST_DIR_IN_DBMANG, exist_ok=True)

#custom qr generator
qr_gen= QRCodeGenerator(base_url="http://example.com", png_files_dir=QR_TEST_DIR_IN_DBMANG)


def setup_temp_db(tmp_path=None):
    #creating temporary database 
    db = DatabaseManager("sqlite:///:memory:")
    return db

def test_insert_update_product():
    db = setup_temp_db()
    
    products = [
        {"ProductID": "P100", "Name": "Laptop Dell", "PriceUSD": "1000.50"},
        {"ProductID": "P101", "Name": "Laptop HP", "PriceUSD": "950.75"},
    ]
    
    #insertion test
    insertion_result= db.insert_or_update_products(products, qr_gen)
    assert insertion_result[0]["action"] == "inserted"
    assert insertion_result[1]["action"] == "inserted"
    
    #update test
    prod_to_update={"ProductID": "P100", "Name": "Laptop Dell", "PriceUSD": "1100.00"}
    update_result= db.insert_or_update_products([prod_to_update], qr_gen)
    assert update_result[0]["action"] == "updated"
    updated_prod = db.get_product_by_id("P100")
    assert updated_prod.price == Decimal("1100.00")
    
    #update test with no changes in database
    prod_no_change = {"ProductID": "P101", "Name": "Laptop HP", "PriceUSD": "950.75"}
    no_change_result= db.insert_or_update_products([prod_no_change], qr_gen)
    assert no_change_result[0]["action"] == "skipped"

def test_get_product_by_id():
    db = setup_temp_db()
    
    product = {"ProductID": "P200", "Name": "Mouse Logitech", "PriceUSD": "25.99"}
    db.insert_or_update_products([product], qr_gen)
    
    retrieved_prod = db.get_product_by_id("P200")
    assert retrieved_prod is not None
    assert retrieved_prod.name == "Mouse Logitech"
    assert retrieved_prod.price == Decimal("25.99")


def test_get_products_by_name():
    db = setup_temp_db()
    
    products = [
        {"ProductID": "P300", "Name": "Keyboard Logitech", "PriceUSD": "45.00"},
        {"ProductID": "P301", "Name": "Keyboard Dell", "PriceUSD": "55.00"},
        {"ProductID": "P302", "Name": "Monitor LG", "PriceUSD": "150.00"},
    ]
    
    db.insert_or_update_products(products, qr_gen)
    
    keyboards = db.get_product_by_name("Keyboard")
    assert len(keyboards) == 2
    ids = [p.product_id for p in keyboards]
    assert "P300" in ids
    assert "P301" in ids
    
    
def test_get_all_products():
    db = setup_temp_db()
    
    products = [
        {"ProductID": "P400", "Name": "Tablet Samsung", "PriceUSD": "300.00"},
        {"ProductID": "P401", "Name": "Tablet Apple", "PriceUSD": "800.00"},
    ]
    db.insert_or_update_products(products, qr_gen)
    
    all_products = db.get_all_products()
    ids = [p.product_id for p in all_products]
    assert "P401" in ids
    assert "P400" in ids
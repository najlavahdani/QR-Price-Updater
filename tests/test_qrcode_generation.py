import os
from src.db.database_manager import DatabaseManager
from src.services.qrcode_generator import QRCodeGenerator

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QR_TEST_DIR= os.path.join(os.path.join(os.path.join(BASE_DIR, "assets"), "qrcodes"), "test")
os.makedirs(QR_TEST_DIR, exist_ok=True)

def setup_temp_db():
    db = DatabaseManager("sqlite:///:memory:")
    return db

def insert_and_update_products_with_custom_qr():
    db = setup_temp_db()
    
    #custom qr generator
    qr_gen= QRCodeGenerator(base_url="http://example.com", png_files_dir=QR_TEST_DIR)

    #new products
    products= [
        {"ProductID": "P900", "Name": "Test Product 1", "PriceUSD": "10.00"},
        {"ProductID": "P901", "Name": "Test Product 2", "PriceUSD": "20.50"},
    ]
    
    #test inserting products with qr codes
    insertion_result = db.insert_or_update_products(products, qr_gen)
    assert insertion_result[0]["action"] == "inserted"
    assert insertion_result[1]["action"] == "inserted"
    
    #checking products qr codes
    for p in products:
        prod= db.get_product_by_id(p["ProductID"])
        assert prod.qr_path is not None
        assert os.path.exists(prod.qr_path)
        assert prod.qr_path.startswith(QR_TEST_DIR)
        print(f"QR for {p['ProductID']} generated at: {prod.qr_path}")
        
    qr_path_before_update= db.get_product_by_id("P900").qr_path 
    #product update without changing QR
    updated_product=  {"ProductID": "P900", "Name": "Test Product 1 Updated", "PriceUSD": "12.00"}
    updating_result= db.insert_or_update_products(updated_product, qr_gen)
    assert updating_result[0]["action"] == "updated"
    
    #checking that the QR code has not been changed
    prod_after_update= db.get_product_by_id("P900")
    qr_path_after_update = db.get_product_by_id("P900").qr_path
    assert qr_path_before_update == qr_path_after_update
    print(f"QR path after update remains: {prod_after_update.qr_path}")
from src.db.database_manager import DatabaseManager
from decimal import Decimal

def setup_temp_db():
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
    insertion_result= db.insert_or_update_products(products)
    assert insertion_result[0]["action"] == "inserted"
    assert insertion_result[1]["action"] == "inserted"
    
    #update test
    prod_to_update={"ProductID": "P100", "Name": "Laptop Dell", "PriceUSD": "1100.00"}
    update_result= db.insert_or_update_products([prod_to_update])
    assert update_result[0]["action"] == "updated"
    updated_prod = db.get_product_by_id("P100")
    assert updated_prod.price == Decimal(1100.00)
    

def test_get_product_by_id():
    db = setup_temp_db()
    
    product = {"ProductID": "P200", "Name": "Mouse Logitech", "PriceUSD": "25.99"}
    db.insert_or_update_products([product])
    
    retrieved_prod = db.get_product_by_id("P200")
    assert retrieved_prod is not None
    assert retrieved_prod.neme == "Mouse Logitech"
    assert retrieved_prod.price == Decimal(25.99)


def test_get_products_by_name():
    db = setup_temp_db()
    
    products = [
        {"ProductID": "P300", "Name": "Keyboard Logitech", "PriceUSD": "45.00"},
        {"ProductID": "P301", "Name": "Keyboard Dell", "PriceUSD": "55.00"},
        {"ProductID": "P302", "Name": "Monitor LG", "PriceUSD": "150.00"},
    ]
    
    db.insert_or_update_products(products)
    
    keyboards = db.get_product_by_name("Keyboard")
    assert len(keyboards) == 2
    ids = [p.product_id for p in keyboards]
    assert "P300" in ids
    assert "P301" in ids
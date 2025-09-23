from src.db.database_manager import DatabaseManager


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
    



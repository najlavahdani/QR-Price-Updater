import unittest
import os
from src.utils.data_loader import load_products_from_excel

class TestDataLoader(unittest.TestCase):
    def test_load_products(self):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__)) #QR price updater
        excel_path = os.path.join(BASE_DIR, "test_data", "products.xlsx") #QR price updater/data/product.xlsx
        products = load_products_from_excel(excel_path)
        self.assertIsInstance(products, list)
        self.assertIn("ProductID", products[0])
        self.assertIn("Name", products[0])
        self.assertIn("PriceUSD", products[0])


if __name__ == "__main__":
    unittest.main()

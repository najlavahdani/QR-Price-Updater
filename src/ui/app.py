import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

from src.utils.data_loader import load_products_from_excel
from src.db.database_manager import DatabaseManager
from src.services.qrcode_generator import QRCodeGenerator

class ProductQRApp:
    def  __init__(self, root):
        self.root = root
        self.root.title("Product QR Manager")
        self.root.geometry("800x600")
        
        #DB manager and QR generator initialization
        self.db_manager = DatabaseManager(qr_base_url="http://QRApp.com")
        self.qr_gen = QRCodeGenerator(base_url="http://QRApp.com")
        
        #create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        #Tab1: import excel
        self.create_tab_import()
        
    
    
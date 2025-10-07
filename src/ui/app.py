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
        
    
    #----------Tab1: import excel----------
    def create_tab_import(self):
        tab_import = ttk.Frame(self.notebook)
        self.notebook.add(tab_import, text="ورود اکسل")
        
        tk.Label(tab_import, text="برای ورود گروهی محصولات، فایل اکسل را آپلود کنید:").pack(pady=10)
        self.entry_file = tk.Entry(tab_import, width=60)
        self.entry_file.pack(pady=5)
        
        tk.Button(tab_import, text="انتخاب فایل", command=self.choose_file).pack(pady=5)
        tk.Button(tab_import, text="وارد کردن", command=self.import_excel).pack(pady=10)
        
    #-----helper funcs-----
    # File chooser button
    def choose_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        self.entry_file.delete(0, tk.END)
        self.entry_file.insert(0, filename)
        
   
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from src.utils.data_loader import load_products_from_excel
from src.db.database_manager import DatabaseManager
from src.services.qrcode_generator import QRCodeGenerator
from src.utils.pdf_utils import create_qr_pdf


class ProductQRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیر کد QR محصولات")
        self.root.geometry("800x600")

        # Initialize DB manager and QR generator
        self.db_manager = DatabaseManager(qr_base_url="http://QRApp.com")
        self.qr_gen = QRCodeGenerator(base_url="http://QRApp.com")

        # Track recently generated QR items (image + name + id)
        self.recent_qr_items = []

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Tab 1: Import Excel
        self.create_tab_import()
        # inside __init__ after self.create_tab_import()
        self.create_tab_add()

    # ---------- Tab 1: Import Excel ----------
    def create_tab_import(self):
        tab_import = ttk.Frame(self.notebook)
        self.notebook.add(tab_import, text="ورود اکسل")

        tk.Label(tab_import, text=":برای ورود گروهی محصولات، فایل اکسل را آپلود کنید").pack(pady=10)
        self.entry_file = tk.Entry(tab_import, width=60)
        self.entry_file.pack(pady=5)

        tk.Button(tab_import, text="انتخاب فایل", command=self.choose_file).pack(pady=5)
        tk.Button(tab_import, text="وارد کردن", command=self.import_excel).pack(pady=10)

        # Add Download PDF button (disabled initially)
        self.download_pdf_btn = tk.Button(
            tab_import,
            text="دانلود PDF کدهای QR",
            command=self.download_qr_pdf,
            state="disabled"
        )
        self.download_pdf_btn.pack(pady=10)

    # ----- Helper Functions -----
    def choose_file(self):
        """Open file dialog to choose Excel file."""
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        self.entry_file.delete(0, tk.END)
        self.entry_file.insert(0, filename)

    def import_excel(self):
        """Load Excel file, validate, insert/update DB, and generate QR codes."""
        file_path = self.entry_file.get()
        if not file_path:
            messagebox.showwarning("هشدار", "لطفاً یک فایل اکسل انتخاب کنید.")
            return

        try:
            # Step 1: Load and validate products from Excel
            products_list = load_products_from_excel(file_path)

            # Step 2: Insert or update products in DB (with QR code generation)
            results = self.db_manager.insert_or_update_products(
                products_list,
                qrcode_generator=self.qr_gen
            )

            # Step 3: Collect new QR code paths
            new_qr_dir = os.path.abspath("assets/MainQRCodes")
            self.recent_qr_items = []  # reset before new import

            for p in products_list:
                pid = p.get("ProductID")
                name = p.get("Name")
                qr_path = os.path.join(new_qr_dir, f"{pid}.png")

                # Only collect newly inserted items
                res = next((r for r in results if r["product_id"] == pid and r["action"] == "inserted"), None)
                if res and os.path.exists(qr_path):
                    self.recent_qr_items.append({
                        "image_path": qr_path,
                        "product_id": pid,
                        "product_name": name
                    })

            # Step 4: Show import summary
            inserted = sum(1 for r in results if r["action"] == "inserted")
            updated = sum(1 for r in results if r["action"] == "updated")
            skipped = sum(1 for r in results if r["action"] == "skipped")

            messagebox.showinfo(
                "نتیجه ورود اطلاعات",
                f"محصولات وارد شده: {inserted}\n"
                f"محصولات بروزرسانی شده: {updated}\n"
                f"محصولات نادیده گرفته شده: {skipped}"
            )

            # Step 5: Enable PDF download button if new QR codes were created
            if self.recent_qr_items:
                self.download_pdf_btn.config(state="normal")
            else:
                self.download_pdf_btn.config(state="disabled")

        except Exception as e:
            messagebox.showerror("خطا", f"خطا در وارد کردن فایل اکسل:\n{e}")

    def download_qr_pdf(self):
        """Combine recent QR codes into a single PDF and let the user save it."""
        if not getattr(self, "recent_qr_items", None):
            messagebox.showwarning("هشدار", "کد QR جدیدی برای دانلود وجود ندارد.")
            return

        save_path = filedialog.asksaveasfilename(
            title="ذخیره PDF کدهای QR",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="QRCodes.pdf"
        )

        if not save_path:
            messagebox.showinfo("لغو شد", "عملیات ذخیره‌سازی لغو شد.")
            return

        try:
            # try to create PDF; pdf_utils will auto-find a TTF font if available
            # you can also pass font_path=r"C:\Windows\Fonts\Tahoma.ttf" explicitly
            create_qr_pdf(self.recent_qr_items, save_path, title="فهرست QR کدها")
            messagebox.showinfo("موفقیت", f"PDF با موفقیت ذخیره شد:\n{save_path}")
        except RuntimeError as re:
            # likely missing font — show clear instructions
            messagebox.showerror(
                "خطا در ساخت PDF",
                "فونت سیستم فارسی را ساپورت نمیکند. tahoma.ttf را دانلود کرده و درمسیر C:\Windows\Fonts\Tahoma.ttf قرار دهید."
            )
        except Exception as e:
            messagebox.showerror("خطا در ساخت PDF", f"خطای غیرمنتظره هنگام ساخت PDF:\n{e}")



    #----------Tab2: Insert single product----------
    def create_tab_add(self):
        tab_add = ttk.Frame(self.notebook)
        self.notebook.add(tab_add, text="درج محصول")

        # Labels & Entries
        tk.Label(tab_add, text="شناسه محصول").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_single_id = tk.Entry(tab_add, width=40)
        self.entry_single_id.grid(row=0, column=1, pady=10)

        tk.Label(tab_add, text="نام محصول").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_single_name = tk.Entry(tab_add, width=40)
        self.entry_single_name.grid(row=1, column=1, pady=10)

        tk.Label(tab_add, text="قیمت محصول").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_single_price = tk.Entry(tab_add, width=40)
        self.entry_single_price.grid(row=2, column=1, pady=10)

        # Insert button
        tk.Button(tab_add, text="درج کردن", command=self.insert_single_product_ui).grid(
            row=3, column=0, columnspan=2, pady=15
        )

        # PDF download button (disabled initially)
        self.download_single_pdf_btn = tk.Button(
            tab_add,
            text="دانلود PDF کد QR محصول",
            command=self.download_single_qr_pdf,
            state="disabled"
        )
        self.download_single_pdf_btn.grid(row=4, column=0, columnspan=2, pady=10)



# ----------------- Run the app -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ProductQRApp(root)
    root.mainloop()

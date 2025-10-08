# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# import os
# from decimal import Decimal

# from src.services.exchange_rate import ExchangeRate
# from src.utils.data_loader import load_products_from_excel
# from src.db.database_manager import DatabaseManager
# from src.services.qrcode_generator import QRCodeGenerator
# from src.utils.pdf_utils import create_qr_pdf


# class ProductQRApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("مدیر کد QR محصولات")
#         self.root.geometry("900x650")

#         # Initialize DB manager and QR generator
#         self.db_manager = DatabaseManager(qr_base_url="http://QRApp.com")
#         self.qr_gen = QRCodeGenerator(base_url="http://QRApp.com")

#         self.recent_qr_items = []
#         self.edited_cells = {}

#         # Create notebook for tabs
#         self.notebook = ttk.Notebook(root)
#         self.notebook.pack(expand=True, fill="both")

#         # Initialize tabs
#         self.create_tab_import()
#         self.create_tab_add()
#         self.create_tab_manage()

#     # ----------------- Tab 1: Import Excel -----------------
#     def create_tab_import(self):
#         tab_import = ttk.Frame(self.notebook)
#         self.notebook.add(tab_import, text="ورود اکسل")

#         tk.Label(tab_import, text=":برای ورود گروهی محصولات، فایل اکسل را آپلود کنید").pack(pady=10)
#         self.entry_file = tk.Entry(tab_import, width=60)
#         self.entry_file.pack(pady=5)

#         tk.Button(tab_import, text="انتخاب فایل", command=self.choose_file).pack(pady=5)
#         tk.Button(tab_import, text="وارد کردن", command=self.import_excel).pack(pady=10)

#         self.download_pdf_btn = tk.Button(
#             tab_import,
#             text="دانلود PDF کدهای QR",
#             command=self.download_qr_pdf,
#             state="disabled",
#         )
#         self.download_pdf_btn.pack(pady=10)

#     def choose_file(self):
#         filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
#         self.entry_file.delete(0, tk.END)
#         self.entry_file.insert(0, filename)

#     def import_excel(self):
#         file_path = self.entry_file.get()
#         if not file_path:
#             messagebox.showwarning("هشدار", "لطفاً یک فایل اکسل انتخاب کنید.")
#             return

#         try:
#             products_list = load_products_from_excel(file_path)
#             results = self.db_manager.insert_or_update_products(
#                 products_list, qrcode_generator=self.qr_gen
#             )

#             new_qr_dir = os.path.abspath("assets/MainQRCodes")
#             self.recent_qr_items = []
#             for p in products_list:
#                 pid = p.get("ProductID")
#                 name = p.get("Name")
#                 qr_path = os.path.join(new_qr_dir, f"{pid}.png")

#                 res = next((r for r in results if r["product_id"] == pid and r["action"] == "inserted"), None)
#                 if res and os.path.exists(qr_path):
#                     self.recent_qr_items.append({
#                         "image_path": qr_path, "product_id": pid, "product_name": name
#                     })

#             inserted = sum(1 for r in results if r["action"] == "inserted")
#             updated = sum(1 for r in results if r["action"] == "updated")
#             skipped = sum(1 for r in results if r["action"] == "skipped")

#             messagebox.showinfo(
#                 "نتیجه ورود اطلاعات",
#                 f"محصولات وارد شده: {inserted}\nمحصولات بروزرسانی شده: {updated}\nمحصولات نادیده گرفته شده: {skipped}"
#             )

#             self.download_pdf_btn.config(
#                 state="normal" if self.recent_qr_items else "disabled"
#             )

#         except Exception as e:
#             messagebox.showerror("خطا", f"خطا در وارد کردن فایل اکسل:\n{e}")

#     def download_qr_pdf(self):
#         if not getattr(self, "recent_qr_items", None):
#             messagebox.showwarning("هشدار", "کد QR جدیدی برای دانلود وجود ندارد.")
#             return

#         save_path = filedialog.asksaveasfilename(
#             title="ذخیره PDF کدهای QR",
#             defaultextension=".pdf",
#             filetypes=[("PDF files", "*.pdf")],
#             initialfile="QRCodes.pdf"
#         )
#         if not save_path:
#             return

#         try:
#             create_qr_pdf(self.recent_qr_items, save_path, title="فهرست QR کدها")
#             messagebox.showinfo("موفقیت", f"PDF با موفقیت ذخیره شد:\n{save_path}")
#         except Exception as e:
#             messagebox.showerror("خطا در ساخت PDF", f"خطا در ساخت PDF:\n{e}")

#     # ----------------- Tab 2: Insert Single Product -----------------
#     def create_tab_add(self):
#         tab_add = ttk.Frame(self.notebook)
#         self.notebook.add(tab_add, text="درج محصول")

#         tk.Label(tab_add, text="شناسه محصول").grid(row=0, column=0, padx=10, pady=10, sticky="e")
#         self.entry_single_id = tk.Entry(tab_add, width=40)
#         self.entry_single_id.grid(row=0, column=1, pady=10)

#         tk.Label(tab_add, text="نام محصول").grid(row=1, column=0, padx=10, pady=10, sticky="e")
#         self.entry_single_name = tk.Entry(tab_add, width=40)
#         self.entry_single_name.grid(row=1, column=1, pady=10)

#         tk.Label(tab_add, text="قیمت محصول").grid(row=2, column=0, padx=10, pady=10, sticky="e")
#         self.entry_single_price = tk.Entry(tab_add, width=40)
#         self.entry_single_price.grid(row=2, column=1, pady=10)

#         tk.Button(tab_add, text="درج کردن", command=self.insert_single_product_ui).grid(
#             row=3, column=0, columnspan=2, pady=15
#         )

#         self.download_single_pdf_btn = tk.Button(
#             tab_add,
#             text="دانلود PDF کد QR محصول",
#             command=self.download_single_qr_pdf,
#             state="disabled"
#         )
#         self.download_single_pdf_btn.grid(row=4, column=0, columnspan=2, pady=10)

#     def insert_single_product_ui(self):
#         pid = self.entry_single_id.get().strip()
#         name = self.entry_single_name.get().strip()
#         price = self.entry_single_price.get().strip()

#         if not pid or not name or not price:
#             messagebox.showwarning("هشدار", "لطفاً تمام فیلدها را پر کنید.")
#             return

#         try:
#             price_decimal = Decimal(price)
#         except Exception:
#             messagebox.showerror("خطا", "قیمت محصول نامعتبر است.")
#             return

#         product = {"ProductID": pid, "Name": name, "PriceUSD": price_decimal}
#         try:
#             result = self.db_manager.insert_single_product(product, qrcode_generator=self.qr_gen)
#             action = result.get("action")
#             reason = result.get("reason", "")
#             messagebox.showinfo("نتیجه درج محصول", f"وضعیت: {action}\n{reason}")

#             qr_dir = os.path.abspath("assets/MainQRCodes")
#             qr_path = os.path.join(qr_dir, f"{pid}.png")
#             if action == "inserted" and os.path.exists(qr_path):
#                 self.recent_qr_items = [{"image_path": qr_path, "product_id": pid, "product_name": name}]
#                 self.download_single_pdf_btn.config(state="normal")
#             else:
#                 self.download_single_pdf_btn.config(state="disabled")

#         except Exception as e:
#             messagebox.showerror("خطا", f"خطا در درج محصول:\n{e}")

#     def download_single_qr_pdf(self):
#         if not getattr(self, "recent_qr_items", None):
#             messagebox.showwarning("هشدار", "کد QR محصول جدیدی برای دانلود وجود ندارد.")
#             return

#         save_path = filedialog.asksaveasfilename(
#             title="ذخیره PDF کد QR محصول",
#             defaultextension=".pdf",
#             filetypes=[("PDF files", "*.pdf")],
#             initialfile=f"{self.recent_qr_items[0]['product_id']}_QR.pdf"
#         )
#         if not save_path:
#             return

#         try:
#             create_qr_pdf(self.recent_qr_items, save_path, title="QR کد محصول")
#             messagebox.showinfo("موفقیت", f"PDF با موفقیت ذخیره شد:\n{save_path}")
#         except Exception as e:
#             messagebox.showerror("خطا در ساخت PDF", f"خطا در ساخت PDF:\n{e}")

#     # ----------------- Tab 3: Manage Products -----------------
#     def create_tab_manage(self):
#         tab_manage = ttk.Frame(self.notebook)
#         self.notebook.add(tab_manage, text="مدیریت محصولات")

#         # Search Controls
#         search_frame = ttk.Frame(tab_manage)
#         search_frame.pack(pady=10)

#         tk.Label(search_frame, text="جستجو بر اساس:").grid(row=0, column=0, padx=5)
#         self.search_type_manage = ttk.Combobox(
#             search_frame, values=["شناسه محصول", "نام محصول"], state="readonly", width=20
#         )
#         self.search_type_manage.current(0)
#         self.search_type_manage.grid(row=0, column=1, padx=5)

#         self.entry_search_manage = tk.Entry(search_frame, width=40)
#         self.entry_search_manage.grid(row=0, column=2, padx=5)

#         tk.Button(search_frame, text="جستجو", command=self.search_products_manage).grid(row=0, column=3, padx=5)

#         # Treeview Table
#         columns = ("ProductID", "Name", "PriceUSD")
#         self.tree_manage = ttk.Treeview(tab_manage, columns=columns, show="headings", height=15)
#         for col, text in zip(columns, ["شناسه", "نام محصول", "قیمت"]):
#             self.tree_manage.heading(col, text=text)
#             self.tree_manage.column(col, width=150, anchor="center")
#         self.tree_manage.pack(expand=True, fill="both", pady=10)

#         # Enable editing
#         self.tree_manage.bind("<Double-1>", self.on_cell_double_click_manage)

#         # Action Buttons
#         btn_frame = ttk.Frame(tab_manage)
#         btn_frame.pack(pady=10)
#         tk.Button(btn_frame, text="ذخیره تغییرات", command=self.save_table_changes).grid(row=0, column=0, padx=10)
#         tk.Button(btn_frame, text="دانلود QR PDF", command=self.download_selected_qr_pdf_manage).grid(row=0, column=1, padx=10)

#     # ----------------- Manage Tab Methods -----------------
#     def search_products_manage(self):
#         search_value = self.entry_search_manage.get().strip()
#         if not search_value:
#             messagebox.showwarning("هشدار", "لطفاً مقدار جستجو را وارد کنید.")
#             return

#         try:
#             if self.search_type_manage.get() == "شناسه محصول":
#                 product = self.db_manager.get_product_by_id(search_value, None)
#                 products = [product] if product else []
#             else:
#                 products = self.db_manager.get_product_by_name(search_value, None)

#             for i in self.tree_manage.get_children():
#                 self.tree_manage.delete(i)

#             for p in products:
#                 self.tree_manage.insert(
#                     "",
#                     tk.END,
#                     values=(p.product_id, p.name, str(p.price), p.qr_path or ""),
#                 )

#         except Exception as e:
#             messagebox.showerror("خطا در جستجو", f"خطا در واکشی داده‌ها:\n{e}")

#     def on_cell_double_click_manage(self, event):
#         region = self.tree_manage.identify_region(event.x, event.y)
#         if region != "cell":
#             return

#         row_id = self.tree_manage.identify_row(event.y)
#         col = self.tree_manage.identify_column(event.x)
#         col_index = int(col.replace("#", "")) - 1
#         if col_index not in (1, 2):  # Only Name, Price editable
#             return

#         x, y, width, height = self.tree_manage.bbox(row_id, col)
#         value = self.tree_manage.set(row_id, column=self.tree_manage["columns"][col_index])

#         entry = tk.Entry(self.tree_manage)
#         entry.place(x=x, y=y, width=width, height=height)
#         entry.insert(0, value)
#         entry.focus()

#         def save_edit(event):
#             new_val = entry.get()
#             entry.destroy()
#             self.tree_manage.set(row_id, column=self.tree_manage["columns"][col_index], value=new_val)
#             self.edited_cells[row_id] = self.tree_manage.item(row_id)["values"]

#         entry.bind("<Return>", save_edit)
#         entry.bind("<FocusOut>", lambda e: entry.destroy())

#     def save_table_changes(self):
#         if not self.edited_cells:
#             messagebox.showinfo("اطلاع", "هیچ تغییری برای ذخیره وجود ندارد.")
#             return

#         try:
#             for row_id, values in self.edited_cells.items():
#                 pid, name, price, _ = values
#                 product = {"ProductID": pid, "Name": name, "PriceUSD": Decimal(price)}
#                 self.db_manager.insert_single_product(product, qrcode_generator=self.qr_gen)
#             messagebox.showinfo("موفقیت", "تغییرات با موفقیت ذخیره شد.")
#             self.edited_cells.clear()
#         except Exception as e:
#             messagebox.showerror("خطا در ذخیره", f"خطا در بروزرسانی محصولات:\n{e}")

#     def download_selected_qr_pdf_manage(self):
#         selected = self.tree_manage.selection()
#         if not selected:
#             messagebox.showwarning("هشدار", "هیچ محصولی انتخاب نشده است.")
#             return

#         item = self.tree_manage.item(selected[0])["values"]
#         product = {"product_id": item[0], "name": item[1], "price_usd": item[2], "qr_path": item[3]}
#         self.download_qr_pdf_for_product(product)

#     def download_qr_pdf_for_product(self, product):
#         if not product.get("qr_path") or not os.path.exists(product["qr_path"]):
#             messagebox.showwarning("هشدار", "فایل QR محصول یافت نشد.")
#             return

#         save_path = filedialog.asksaveasfilename(
#             title="ذخیره PDF کد QR محصول",
#             defaultextension=".pdf",
#             filetypes=[("PDF files", "*.pdf")],
#             initialfile=f"{product['product_id']}_QR.pdf"
#         )
#         if not save_path:
#             return

#         try:
#             qr_items = [{"image_path": product["qr_path"], "product_id": product["product_id"], "product_name": product["name"]}]
#             create_qr_pdf(qr_items, save_path, title="QR کد محصول")
#             messagebox.showinfo("موفقیت", f"PDF با موفقیت ذخیره شد:\n{save_path}")
#         except Exception as e:
#             messagebox.showerror("خطا در ساخت PDF", f"خطا در ساخت PDF:\n{e}")


# # ----------------- Run the app -----------------
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ProductQRApp(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from decimal import Decimal

from src.services.exchange_rate import ExchangeRate
from src.utils.data_loader import load_products_from_excel
from src.db.database_manager import DatabaseManager
from src.services.qrcode_generator import QRCodeGenerator
from src.utils.pdf_utils import create_qr_pdf


class ProductQRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیر کد QR محصولات")
        self.root.geometry("900x650")

        # services / managers
        self.db_manager = DatabaseManager(qr_base_url="http://QRApp.com")
        self.qr_gen = QRCodeGenerator(base_url="http://QRApp.com")
        self.exchange_service = ExchangeRate()

        # transient state
        self.recent_qr_items = []
        self.edited_cells = {}

        # main UI
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.create_tab_import()
        self.create_tab_add()
        self.create_tab_manage()
        self.create_tab_update_currency()

    # ----------------- Tab 1: Import Excel -----------------
    def create_tab_import(self):
        tab_import = ttk.Frame(self.notebook)
        self.notebook.add(tab_import, text="ورود اکسل")

        tk.Label(tab_import, text=":برای ورود گروهی محصولات، فایل اکسل را آپلود کنید").pack(pady=10)
        self.entry_file = tk.Entry(tab_import, width=60)
        self.entry_file.pack(pady=5)

        tk.Button(tab_import, text="انتخاب فایل", command=self.choose_file).pack(pady=5)
        tk.Button(tab_import, text="وارد کردن", command=self.import_excel).pack(pady=10)

        self.download_pdf_btn = tk.Button(
            tab_import,
            text="دانلود PDF کدهای QR",
            command=self.download_qr_pdf,
            state="disabled",
        )
        self.download_pdf_btn.pack(pady=10)

    def choose_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        self.entry_file.delete(0, tk.END)
        self.entry_file.insert(0, filename)

    def import_excel(self):
        file_path = self.entry_file.get().strip()
        if not file_path:
            messagebox.showwarning("هشدار", "لطفاً یک فایل اکسل انتخاب کنید.")
            return

        try:
            products_list = load_products_from_excel(file_path)
            results = self.db_manager.insert_or_update_products(products_list, qrcode_generator=self.qr_gen)

            new_qr_dir = os.path.abspath("assets/MainQRCodes")
            self.recent_qr_items = []
            for p in products_list:
                pid = str(p.get("ProductID")).strip()
                name = str(p.get("Name")).strip()
                qr_path = os.path.join(new_qr_dir, f"{pid}.png")

                res = next((r for r in results if r.get("product_id") == pid and r.get("action") == "inserted"), None)
                if res and os.path.exists(qr_path):
                    self.recent_qr_items.append({
                        "image_path": qr_path,
                        "product_id": pid,
                        "product_name": name
                    })

            inserted = sum(1 for r in results if r.get("action") == "inserted")
            updated = sum(1 for r in results if r.get("action") == "updated")
            skipped = sum(1 for r in results if r.get("action") == "skipped")

            messagebox.showinfo(
                "نتیجه ورود اطلاعات",
                f"محصولات وارد شده: {inserted}\nمحصولات بروزرسانی شده: {updated}\nمحصولات نادیده گرفته شده: {skipped}"
            )

            self.download_pdf_btn.config(state="normal" if self.recent_qr_items else "disabled")

        except Exception as e:
            messagebox.showerror("خطا", f"خطا در وارد کردن فایل اکسل:\n{e}")

    def download_qr_pdf(self):
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
            return

        try:
            create_qr_pdf(self.recent_qr_items, save_path, title="فهرست QR کدها")
            messagebox.showinfo("موفقیت", f"PDF با موفقیت ذخیره شد:\n{save_path}")
        except Exception as e:
            messagebox.showerror("خطا در ساخت PDF", f"خطا در ساخت PDF:\n{e}")

    # ----------------- Tab 2: Insert Single Product -----------------
    def create_tab_add(self):
        tab_add = ttk.Frame(self.notebook)
        self.notebook.add(tab_add, text="درج محصول")

        tk.Label(tab_add, text="شناسه محصول").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_single_id = tk.Entry(tab_add, width=40)
        self.entry_single_id.grid(row=0, column=1, pady=10)

        tk.Label(tab_add, text="نام محصول").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_single_name = tk.Entry(tab_add, width=40)
        self.entry_single_name.grid(row=1, column=1, pady=10)

        tk.Label(tab_add, text="قیمت محصول").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_single_price = tk.Entry(tab_add, width=40)
        self.entry_single_price.grid(row=2, column=1, pady=10)

        tk.Button(tab_add, text="درج کردن", command=self.insert_single_product_ui).grid(
            row=3, column=0, columnspan=2, pady=15
        )

        self.download_single_pdf_btn = tk.Button(
            tab_add,
            text="دانلود PDF کد QR محصول",
            command=self.download_single_qr_pdf,
            state="disabled"
        )
        self.download_single_pdf_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def insert_single_product_ui(self):
        pid = self.entry_single_id.get().strip()
        name = self.entry_single_name.get().strip()
        price = self.entry_single_price.get().strip()

        if not pid or not name or not price:
            messagebox.showwarning("هشدار", "لطفاً تمام فیلدها را پر کنید.")
            return

        try:
            price_decimal = Decimal(price)
        except Exception:
            messagebox.showerror("خطا", "قیمت محصول نامعتبر است.")
            return

        product = {"ProductID": pid, "Name": name, "PriceUSD": price_decimal}
        try:
            result = self.db_manager.insert_single_product(product, qrcode_generator=self.qr_gen)
            action = result.get("action")
            reason = result.get("reason", "")
            messagebox.showinfo("نتیجه درج محصول", f"وضعیت: {action}\n{reason}")

            # track qr png if created
            qr_dir = os.path.abspath("assets/MainQRCodes")
            qr_path = os.path.join(qr_dir, f"{pid}.png")
            if action == "inserted" and os.path.exists(qr_path):
                self.recent_qr_items = [{"image_path": qr_path, "product_id": pid, "product_name": name}]
                self.download_single_pdf_btn.config(state="normal")
            else:
                self.download_single_pdf_btn.config(state="disabled")

        except Exception as e:
            messagebox.showerror("خطا", f"خطا در درج محصول:\n{e}")

    def download_single_qr_pdf(self):
        if not getattr(self, "recent_qr_items", None):
            messagebox.showwarning("هشدار", "کد QR محصول جدیدی برای دانلود وجود ندارد.")
            return

        save_path = filedialog.asksaveasfilename(
            title="ذخیره PDF کد QR محصول",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"{self.recent_qr_items[0]['product_id']}_QR.pdf"
        )
        if not save_path:
            return

        try:
            create_qr_pdf(self.recent_qr_items, save_path, title="QR کد محصول")
            messagebox.showinfo("موفقیت", f"PDF با موفقیت ذخیره شد:\n{save_path}")
        except Exception as e:
            messagebox.showerror("خطا در ساخت PDF", f"خطا در ساخت PDF:\n{e}")

    # ----------------- Tab 3: Manage Products -----------------
    def create_tab_manage(self):
        tab_manage = ttk.Frame(self.notebook)
        self.notebook.add(tab_manage, text="مدیریت محصولات")

        # Search Controls
        search_frame = ttk.Frame(tab_manage)
        search_frame.pack(pady=10, fill="x", padx=8)

        tk.Label(search_frame, text="جستجو بر اساس:").grid(row=0, column=0, padx=5)
        self.search_type_manage = ttk.Combobox(
            search_frame, values=["شناسه محصول", "نام محصول"], state="readonly", width=20
        )
        self.search_type_manage.current(0)
        self.search_type_manage.grid(row=0, column=1, padx=5)

        self.entry_search_manage = tk.Entry(search_frame, width=40)
        self.entry_search_manage.grid(row=0, column=2, padx=5)

        tk.Button(search_frame, text="جستجو", command=self.search_products_manage).grid(row=0, column=3, padx=5)

        # Treeview Table
        columns = ("ProductID", "Name", "PriceUSD", "QRPath")
        self.tree_manage = ttk.Treeview(tab_manage, columns=columns, show="headings", height=15)
        self.tree_manage.heading("ProductID", text="شناسه")
        self.tree_manage.heading("Name", text="نام محصول")
        self.tree_manage.heading("PriceUSD", text="قیمت")
        self.tree_manage.heading("QRPath", text="")  # hidden/aux column

        self.tree_manage.column("ProductID", width=160, anchor="center")
        self.tree_manage.column("Name", width=320, anchor="w")
        self.tree_manage.column("PriceUSD", width=120, anchor="e")
        self.tree_manage.column("QRPath", width=0, stretch=False)  # hide the path column

        self.tree_manage.pack(expand=True, fill="both", pady=10, padx=8)

        # Enable editing (double click name/price)
        self.tree_manage.bind("<Double-1>", self.on_cell_double_click_manage)

        # Action Buttons
        btn_frame = ttk.Frame(tab_manage)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="ذخیره تغییرات", command=self.save_table_changes).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="دانلود QR PDF (ردیف انتخابی)", command=self.download_selected_qr_pdf_manage).grid(
            row=0, column=1, padx=10
        )

    def search_products_manage(self):
        search_value = self.entry_search_manage.get().strip()
        if not search_value:
            messagebox.showwarning("هشدار", "لطفاً مقدار جستجو را وارد کنید.")
            return

        try:
            if self.search_type_manage.get() == "شناسه محصول":
                product = self.db_manager.get_product_by_id(search_value, None)
                products = [product] if product else []
            else:
                products = self.db_manager.get_product_by_name(search_value, None)

            # clear
            for i in self.tree_manage.get_children():
                self.tree_manage.delete(i)

            for p in products:
                price_val = getattr(p, "price", None) or getattr(p, "price_usd", None) or 0
                qr_path = getattr(p, "qr_path", "") or ""
                self.tree_manage.insert(
                    "",
                    tk.END,
                    values=(p.product_id, p.name, str(price_val), qr_path),
                )

        except Exception as e:
            messagebox.showerror("خطا در جستجو", f"خطا در واکشی داده‌ها:\n{e}")

    def on_cell_double_click_manage(self, event):
        region = self.tree_manage.identify_region(event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree_manage.identify_row(event.y)
        col = self.tree_manage.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1
        if col_index not in (1, 2):  # Only Name (col 1) and Price (col 2) editable
            return

        x, y, width, height = self.tree_manage.bbox(row_id, col)
        # current value
        current_vals = list(self.tree_manage.item(row_id, "values"))
        old_value = current_vals[col_index]

        entry = tk.Entry(self.tree_manage)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, old_value)
        entry.focus()

        def save_edit(event):
            new_val = entry.get().strip()
            entry.destroy()
            current_vals[col_index] = new_val
            self.tree_manage.item(row_id, values=current_vals)
            # mark row as edited
            self.edited_cells[row_id] = current_vals

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def save_table_changes(self):
        if not self.edited_cells:
            messagebox.showinfo("اطلاع", "هیچ تغییری برای ذخیره وجود ندارد.")
            return

        try:
            for row_id, values in self.edited_cells.items():
                pid, name, price, _qr = values
                # validate price
                try:
                    price_decimal = Decimal(str(price))
                except Exception:
                    raise ValueError(f"قیمت نامعتبر برای محصول {pid}: {price}")

                product = {"ProductID": pid, "Name": name, "PriceUSD": price_decimal}
                self.db_manager.insert_single_product(product, qrcode_generator=self.qr_gen)

            messagebox.showinfo("موفقیت", "تغییرات با موفقیت ذخیره شد.")
            self.edited_cells.clear()
        except Exception as e:
            messagebox.showerror("خطا در ذخیره", f"خطا در بروزرسانی محصولات:\n{e}")

    def download_selected_qr_pdf_manage(self):
        selected = self.tree_manage.selection()
        if not selected:
            messagebox.showwarning("هشدار", "هیچ محصولی انتخاب نشده است.")
            return

        item = self.tree_manage.item(selected[0])["values"]
        product = {"product_id": item[0], "name": item[1], "price_usd": item[2], "qr_path": item[3]}
        self.download_qr_pdf_for_product(product)

    def download_qr_pdf_for_product(self, product):
        qr_path = product.get("qr_path")
        if not qr_path or not os.path.exists(qr_path):
            messagebox.showwarning("هشدار", "فایل QR محصول یافت نشد.")
            return

        save_path = filedialog.asksaveasfilename(
            title="ذخیره PDF کد QR محصول",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"{product['product_id']}_QR.pdf"
        )
        if not save_path:
            return

        try:
            qr_items = [{
                "image_path": qr_path,
                "product_id": product["product_id"],
                "product_name": product["name"]
            }]
            create_qr_pdf(qr_items, save_path, title="QR کد محصول")
            messagebox.showinfo("موفقیت", f"PDF با موفقیت ذخیره شد:\n{save_path}")
        except Exception as e:
            messagebox.showerror("خطا در ساخت PDF", f"خطا در ساخت PDF:\n{e}")

    # ----------------- Tab 4: Update Currency Rate -----------------
    def create_tab_update_currency(self):
        tab_update_currency = ttk.Frame(self.notebook)
        self.notebook.add(tab_update_currency, text="بروزرسانی نرخ")

        tk.Label(tab_update_currency, text="نرخ ارز جدید (مقدار عددی)").pack(pady=10)
        self.entry_currency = tk.Entry(tab_update_currency, width=20)
        self.entry_currency.pack(pady=5)

        btn_frame = ttk.Frame(tab_update_currency)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="نمایش نرخ فعلی", command=self.show_current_rate).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="بروزرسانی", command=self.update_currency_rate).grid(row=0, column=1, padx=8)

        self.lbl_current_rate = tk.Label(tab_update_currency, text="نرخ فعلی: ---")
        self.lbl_current_rate.pack(pady=8)

    def show_current_rate(self):
        try:
            rate = self.exchange_service.get_rate()
            # show nicely formatted
            try:
                # if rate is Decimal
                rate_num = float(rate)
            except Exception:
                rate_num = rate
            self.lbl_current_rate.config(text=f"نرخ فعلی: {rate_num}")
        except ValueError:
            self.lbl_current_rate.config(text="نرخ فعلی: ثبت نشده")
            messagebox.showwarning("اطلاع", "هیچ نرخی در دیتابیس ثبت نشده است.")
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در دریافت نرخ:\n{e}")

    def update_currency_rate(self):
        new_rate_str = self.entry_currency.get().strip()
        if not new_rate_str:
            messagebox.showwarning("هشدار", "لطفاً نرخ جدید را وارد کنید.")
            return

        try:
            new_rate = Decimal(new_rate_str)
        except Exception:
            messagebox.showerror("خطا", "مقدار نرخ وارد شده عدد صحیح نیست.")
            return

        try:
            setting = self.exchange_service.set_rate(new_rate)
            self.lbl_current_rate.config(text=f"نرخ فعلی: {setting.exchange_rate}")
            messagebox.showinfo("موفقیت", "نرخ ارز با موفقیت بروزرسانی شد.")
            self.entry_currency.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بروزرسانی نرخ:\n{e}")

# ----------------- Tab 5: View All Products -----------------
    def create_tab_list_all(self):
        tab_list = ttk.Frame(self.notebook)
        self.notebook.add(tab_list, text="لیست محصولات")

        # --- Top Action Buttons ---
        btn_frame = ttk.Frame(tab_list)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="بروزرسانی لیست", command=self.load_all_products).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="ذخیره تغییرات", command=self.save_all_table_changes).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="حذف محصول", command=self.delete_selected_product).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="دانلود QR PDF", command=self.download_selected_qr_pdf_all).grid(row=0, column=3, padx=5)

        # --- Product Table ---
        columns = ("ProductID", "Name", "PriceUSD")
        self.tree_list_all = ttk.Treeview(tab_list, columns=columns, show="headings", height=20)

        for col, text in zip(columns, ["شناسه", "نام محصول", "قیمت (دلار)"]):
            self.tree_list_all.heading(col, text=text)
            self.tree_list_all.column(col, width=200, anchor="center")

        self.tree_list_all.pack(expand=True, fill="both", pady=10)

        # Bind editing
        self.tree_list_all.bind("<Double-1>", self.on_cell_double_click_all)

        # Track edits
        self.edited_cells_all = {}

        # Load data initially
        self.load_all_products()

# ----------------- Run the app -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ProductQRApp(root)
    root.mainloop()

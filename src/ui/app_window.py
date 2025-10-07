import tkinter as tk
from tkinter import ttk, filedialog

#main window
root = tk.Tk()
root.title("Product QR Manager")
root.geometry("800x600") #window size

#notebook for tabs
notebook=ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

#-----------Tab1-----------
#import excel
tab_import = ttk.Frame(notebook)
notebook.add(tab_import, text="ورود اکسل")

tk.Label(tab_import, text="برای ورود گروهی داده ها، فایل اکسل را آپلود کنید:")
entry_file= tk.Entry(tab_import, width=60)
entry_file.pack(pady=5)
def choose_file():
    filename= filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, filename)
tk.Button(tab_import, text="انتخاب فایل", command=choose_file).pack(pady=5)
tk.Button(tab_import, text="وارد کردن").pack(pady=10)


#----------Tab2-----------
#insert single product
tab_add= ttk.Frame(notebook)
notebook.add(tab_add, text="درج محصول")

tk.Label(tab_add, text="شناسه محصول").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_id= tk.Entry(tab_add, width=40)
entry_id.grid(row=0, column=1, pady=10)

tk.Label(tab_add, text="نام محصول").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_id= tk.Entry(tab_add, width=40)
entry_id.grid(row=1, column=1, pady=10)

tk.Label(tab_add, text="قیمت محصول").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_id= tk.Entry(tab_add, width=40)
entry_id.grid(row=2, column=1, pady=10)

tk.Button(tab_add, text="درج کردن").grid(row=3, column=0, columnspan=2, pady=10)


#----------Tab3----------
#search product
tab_search=ttk.Frame(notebook)
notebook.add(tab_search, text="جستجوی محصول")

tk.Label(tab_search, text="نام یا شناسه محصول را وارد کنید").pack(pady=10)
entry_search = tk.Entry(tab_search, width=50)
entry_search.pack(pady=5)
tk.Button(tab_search, text="جستجو").pack(pady=5)

#search result table
tree_search = ttk.Treeview(tab_search, columns=("ProductID", "Name", "PriceUSD"), show='headings')
tree_search.heading("ProductID", text="شناسه محصول")
tree_search.heading("Name", text="نام محصول")
tree_search.heading("PriceUSD", text="قیمت")
tree_search.pack(expand=True, fill='both', pady=10)


#-----------Tab4-----------
tab_update_currency = ttk.Frame(notebook)
notebook.add(tab_update_currency, text="بروزرسانی نرخ")

tk.Label(tab_update_currency, text="نرخ ارز جدید").pack(pady=10)
entry_currency = tk.Entry(tab_update_currency, width=20)
entry_currency.pack(pady=5)
tk.Button(tab_update_currency, text="بروزرسانی").pack(pady=10)

#run the window
root.mainloop()


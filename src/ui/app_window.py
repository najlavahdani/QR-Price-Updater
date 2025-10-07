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


#run the window
root.mainloop()
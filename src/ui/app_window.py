import tkinter as tk
from tkinter import ttk, filedialog

#main window
root = tk.Tk()
root.title("Product QR Manager")
root.geometry("800x600") #window size

#notebook for tabs
notebook=ttk.Notebook(root)
notebook.pack(expand=True, fill='both')


import os

folders = [
    "src",
    "data",
    "src/db",
    "src/utils",
    "src/ui",
    "assets",
    "assets/qrcodes"
]


for folder in folders:
    os.makedirs(folder, exist_ok=True)
    

# for packaging
open("src/__init__.py", "a").close()
open("src/db/__init__.py", "a").close()
open("src/utils/__init__.py", "a").close()

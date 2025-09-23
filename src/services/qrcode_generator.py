import os

class QRCodeGenerator:
    def __init__(self, base_url: str):
        root_path= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
        self.output_dir= os.path.join(os.path.join(root_path, "assets"), "qrcodes")
        
        self.base_url= base_url
        os.makedirs(self.output_dir, exist_ok=True)
import os
import qrcode

class QRCodeGenerator:
    def __init__(self, base_url: str, png_files_dir: str= "C:\\Users\\Najla\\Desktop\\QR price updater\\assets\\MainQRCodes"): 
        self.base_url= base_url
        
        if png_files_dir:
            #costum path
            self.output_dir= png_files_dir
        else:
            #default path
            root_path= os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
            self.output_dir= os.path.join(os.path.join(root_path, "assets"), "qrcodes")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_qr(self, product_id: str) -> str:
        url =f"{self.base_url}/product/{product_id}"
        #path to save the qr code images
        file_path= os.path.join(self.output_dir, f"{product_id}.png")
        
        #generating qr
        img = qrcode.make(url)
        img.save(file_path)
        
        return file_path
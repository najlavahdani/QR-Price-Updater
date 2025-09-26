import cv2

def read_image(path):
    img = cv2.imread(path) #img = (height, width, channels)
    if img is None: #invalid oath
        raise FileNotFoundError(f"Image not found: {path}")
    return img 

#Convert to grayscale color space for faster and more accurate OCR
def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
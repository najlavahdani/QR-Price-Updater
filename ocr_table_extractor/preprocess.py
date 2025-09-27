import cv2
import numpy as np

class Preprocessor:
    def __init__(self, resize_if_small=True):
        self.resize_if_small= resize_if_small
            
def read_image(path):
    img = cv2.imread(path) #img = (height, width, channels)
    if img is None: #invalid oath
        raise FileNotFoundError(f"Image not found: {path}")
    return img 

#Convert to grayscale color space for faster and more accurate OCR
def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#retation correction function
def deskew(gray):
    coords= np.column_stack(np.where(gray<255)) #It stores the coordinates of all pixels that are not pure white in a two-dimensional array as (x, y).
    if coords.size == 0: #Completely white image 
        return gray
    angle= cv2.minAreaRect(coords)[-1]
    #adjust the angle so that the text is almost horizontal
    if angle < -45:
        angle = -(90+angle)
    else: 
        angle = -angle
    (h, w)= gray.shape[:2] 
    center = (w//2 , h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(gray,M, (w,h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

#Converts the input image into a high-contrast binary (black and white) image.
def enhance_for_orc(gray):
    h, w = gray.shape
    #If the image is small, it doubles it so that OCR works better.
    if max(h, w)< 100:
        gray = cv2.resize(gray, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
        blur= cv2.GaussianBlur(gray, (3,3), 0)
        return cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
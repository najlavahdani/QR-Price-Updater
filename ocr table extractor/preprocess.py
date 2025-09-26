import cv2

def read_image(path):
    img = cv2.imread(path) #img = (height, width, channels)
    if img is None: #invalid oath
        raise FileNotFoundError(f"Image not found: {path}")
    return img 
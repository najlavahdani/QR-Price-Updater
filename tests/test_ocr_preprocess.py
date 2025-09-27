from ocr_table_extractor.preprocess import Preprocessor
import pytest
import os 
import numpy as np
import cv2

@pytest.fixture
def tmp_image_path():
    os.mkdir("tests/tests_outputs/output_images", exist_ok=True)
    path = "tests/output_images/white_img.jpg"
    img = np.full((50, 50, 3), 255, dtype=np.uint8)
    cv2.imwrite(path, img)
    return path
    
def test_read_image_valid(tmp_image_path):
    p= Preprocessor()
    img = p.read_image(tmp_image_path) #completely white img's (height, width, channels)
    assert isinstance(img, np.ndarray)
    assert img.shape[0] > 0 and img.shape[1] > 0
      
def test_read_image_invalid(tmp_image_path):
    p = Preprocessor()
    with pytest.raises(FileNotFoundError):
        p.read_image("non_existent_file.jpg")
        
def test_to_grayscale(tmp_image_path):
    p= Preprocessor()
    img= p.read_image(tmp_image_path)
    gray= p.to_grayscale(img)
    assert len(gray.shape) == 2 #sigle-channel image
    assert gray.dtype == np.uint8 #the data type is correct and complies with the OpenCV standard
    assert np.all(gray==255) #stay completely white
    
def test_deskew_white_image(tmp_image_path):
    p =Preprocessor()
    img = p.read_image(tmp_image_path)
    gray = p.to_grayscale(img)
    result = p.deskew(gray)
    #for white images it shouldn't  be changed
    assert result.shape == gray.shape
    assert np.all(result == gray)
    
def test_deskew_rotated_text():
    p = Preprocessor()
    #gray img with small text
    img = np.full((100,200), 255, dtype=np.uint8)
    cv2.putText(img, "Test", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,), 3, cv2.LINE_AA)
    #30 degree rotation
    M = cv2.getRotationMatrix2D((100, 50), 30, 1)
    rotated = cv2.warpAffine(img, M, (200,100), borderValue=255)
    out= p.deskew(rotated)
    assert out.shape == rotated.shape
    assert np.any(out<255)
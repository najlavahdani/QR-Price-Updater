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
    

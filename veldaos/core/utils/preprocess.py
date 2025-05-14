import cv2
import numpy as np
from PIL import Image
from typing import Union, Tuple

def preprocess_image(image: Union[Image.Image, np.ndarray], method: str = "default") -> np.ndarray:
    """
    Preprocess an image for OCR using various methods.
    Supported methods: adaptive_threshold, sharpen, contrast, denoise, morphology, llm_optimized, default
    Args:
        image: PIL Image or numpy array
        method: Preprocessing method to use
    Returns:
        Preprocessed image as numpy array
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image
    
    if method == "adaptive_threshold":
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    elif method == "sharpen":
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        return cv2.filter2D(img_array, -1, kernel)
    elif method == "contrast":
        if len(img_array.shape) == 3:
            lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            merged = cv2.merge((cl,a,b))
            return cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)
        else:
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            return clahe.apply(img_array)
    elif method == "denoise":
        if len(img_array.shape) == 3:
            return cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)
        else:
            return cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
    elif method == "morphology":
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        kernel = np.ones((1,1), np.uint8)
        return cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    elif method == "llm_optimized":
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        binary = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        mean_value = np.mean(binary)
        if mean_value < 127:
            binary = cv2.bitwise_not(binary)
        kernel = np.ones((2,2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        return cleaned
    else:
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary 
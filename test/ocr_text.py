import time
import os
import sys
import cv2
import numpy as np
from PIL import Image
import io
import mss
import mss.tools
from datetime import datetime
from loguru import logger
from typing import List, Dict

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from veldaos.core.utils.pytesseractocr import PyTesseractOCR
from veldaos.core.utils.preprocess import preprocess_image

def draw_boxes(image: np.ndarray, text_elements: list, output_path: str):
    """Draw bounding boxes on the image and save it."""
    # Convert to RGB if grayscale
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    
    # Draw boxes
    for elem in text_elements:
        x, y, w, h = elem['x'], elem['y'], elem['width'], elem['height']
        text = elem['text']
        
        # Draw rectangle
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Draw text
        cv2.putText(image, text, (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Save image
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

def merge_close_text(text_elements: List[Dict[str, int]]) -> List[Dict[str, int]]:
    merged_elements = []
    used_indices = set()

    for i, elem1 in enumerate(text_elements):
        if i in used_indices:
            continue
        x1, y1, w1, h1 = elem1['x'], elem1['y'], elem1['width'], elem1['height']
        text1 = elem1['text']

        for j, elem2 in enumerate(text_elements[i+1:], start=i+1):
            if j in used_indices:
                continue
            x2, y2, w2, h2 = elem2['x'], elem2['y'], elem2['width'], elem2['height']
            text2 = elem2['text']

            # Check if boxes are within 10 pixels horizontally
            distance = min(abs(x1 - (x2 + w2)), abs(x2 - (x1 + w1)))
            if distance <= 10:
                # Check if boxes are roughly on same vertical level
                y_diff = abs(y1 - y2 - 5)
                if y_diff < max(h1, h2) / 2:
                    # Merge boxes
                    new_x = min(x1, x2)
                    new_y = min(y1, y2)
                    new_w = max(x1 + w1, x2 + w2) - new_x
                    new_h = max(y1 + h1, y2 + h2) - new_y
                    new_text = text1 + ' ' + text2

                    # Update elem1
                    elem1 = {'text': new_text, 'x': new_x, 'y': new_y, 'width': new_w, 'height': new_h}
                    used_indices.add(j)

        merged_elements.append(elem1)
        used_indices.add(i)

    return merged_elements

def merge_overlapping_boxes(text_elements: List[Dict[str, int]]) -> List[Dict[str, int]]:
    merged_elements = []
    used_indices = set()

    for i, elem1 in enumerate(text_elements):
        if i in used_indices:
            continue
        x1, y1, w1, h1 = elem1['x'], elem1['y'], elem1['width'], elem1['height']
        text1 = elem1['text']

        for j, elem2 in enumerate(text_elements[i+1:], start=i+1):
            if j in used_indices:
                continue
            x2, y2, w2, h2 = elem2['x'], elem2['y'], elem2['width'], elem2['height']
            text2 = elem2['text']

            # Calculate horizontal overlap
            tolerance = 10
            x1_left = x1 - tolerance
            x1_right = x1 + w1 + tolerance
            x2_left = x2 - tolerance
            x2_right = x2 + w2 + tolerance
            if (x1_right >= x2_left and x1_left <= x2_right) or (x2_right >= x1_left and x2_left <= x1_right):
                # Calculate height overlap
                overlap_height = min(y1 + h1, y2 + h2) - max(y1, y2)
                if overlap_height > 0:
                    overlap_ratio = overlap_height / min(h1, h2)
                    if overlap_ratio > 0:
                        # Merge boxes
                        new_x = min(x1, x2)
                        new_y = min(y1, y2)
                        new_w = max(x1 + w1, x2 + w2) - new_x
                        new_h = min(y1 + h1, y2 + h2) - new_y
                        new_text = text1 + ' ' + text2

                        # Update elem1
                        elem1 = {'text': new_text, 'x': new_x, 'y': new_y, 'width': new_w, 'height': new_h}
                        used_indices.add(j)

        merged_elements.append(elem1)
        used_indices.add(i)

    return merged_elements

def ocr_compressed_images(screenshot: bytes):
    """Test OCR on different compressed versions of the same image."""
    # Initialize OCR
    ocr = PyTesseractOCR()
    
    # Convert screenshot to PIL Image
    image = Image.open(io.BytesIO(screenshot))
    
    # Create base screenshots directory
    base_dir = 'test/screenshots'
    os.makedirs(base_dir, exist_ok=True)
    
    # Save original screenshot
    original_path = os.path.join(base_dir, "original.png")
    image.save(original_path)
    
    # Test different compression methods
    methods = [
        "contrast",
        "llm_optimized"
    ]
    
    results = {}
    for method in methods:
        print(f"\nProcessing {method}...")
        method_dir = os.path.join(base_dir, method)
        os.makedirs(method_dir, exist_ok=True)
        
        # Time compression
        compression_start = time.time()
        processed_image = preprocess_image(image, method)
        compression_time = time.time() - compression_start
        
        # Save processed image
        processed_path = os.path.join(method_dir, f"{method}_processed.png")
        Image.fromarray(processed_image).save(processed_path)
        
        # Convert processed image to bytes for OCR
        img_byte_arr = io.BytesIO()
        Image.fromarray(processed_image).save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Time OCR
        ocr_start = time.time()
        text_elements = ocr.perform_ocr(img_byte_arr, preprocess_method=method)
        ocr_time = time.time() - ocr_start
        
        # Save OCR image with boxes
        ocr_path = os.path.join(method_dir, f"{method}_ocr_boxes.png")
        draw_boxes(np.array(processed_image), text_elements, ocr_path)
        
        # Save results
        results[method] = {
            'text_elements': text_elements,
            'processed_path': processed_path,
            'ocr_path': ocr_path,
            'compression_time': compression_time,
            'ocr_time': ocr_time
        }
        
        # Log timing information
        logger.info(f"{method} - Compression time: {compression_time:.2f}s, OCR time: {ocr_time:.2f}s")
        print(f"Found {len(text_elements)} text elements")
    
    return results

def main():
    print("Waiting 3 seconds before taking screenshot...")
    time.sleep(3)
    
    # Take screenshot using mss
    with mss.mss() as sct:
        # Capture the entire screen
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        
        # Convert to bytes
        img_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)
    
    # Run OCR on compressed images
    results = ocr_compressed_images(img_bytes)
    
    # Print summary of results
    print("\nOCR Results Summary:")
    for method, result in results.items():
        print(f"\n{method}:")
        print(f"Compression time: {result['compression_time']:.2f}s")
        print(f"OCR time: {result['ocr_time']:.2f}s")
        print(f"Number of text elements found: {len(result['text_elements'])}")

if __name__ == "__main__":
    main() 
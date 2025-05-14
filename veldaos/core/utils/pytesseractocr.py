import pytesseract
from loguru import logger
from typing import List, Dict
import cv2
import numpy as np
from PIL import Image
import io
from veldaos.core.utils.preprocess import preprocess_image

class PyTesseractOCR:
    def __init__(self, quality=1.0):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.quality = quality
        self.gray_mode = True

    def perform_ocr(self, screenshot: bytes, preprocess_method: str = "contrast") -> List[Dict[str, int]]:
        # Convert screenshot to PIL Image
        image = Image.open(io.BytesIO(screenshot))
        # Preprocess image using the selected method
        processed = preprocess_image(image, preprocess_method)
        # Convert back to PIL Image for pytesseract
        pil_processed = Image.fromarray(processed)
        # Perform OCR
        ocr_data = pytesseract.image_to_data(pil_processed, output_type=pytesseract.Output.DICT)
        # Extract text elements
        text_elements = []
        for i, text in enumerate(ocr_data['text']):
            if text.strip():
                x = ocr_data['left'][i]
                y = ocr_data['top'][i]
                w = ocr_data['width'][i]
                h = ocr_data['height'][i]
                text_elements.append({
                    'text': text,
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h
                })
        self.draw_boxes("annotated", screenshot, text_elements)
        merged_elements = self.merge_overlapping_boxes(text_elements)
        self.draw_boxes("merged", screenshot, merged_elements)
        merged_close_elements = self.merge_close_text(merged_elements)
        self.draw_boxes("merged_close", screenshot, merged_close_elements)
        return merged_close_elements

    def merge_close_text(self, text_elements: List[Dict[str, int]]) -> List[Dict[str, int]]:
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

                # if len(merged_elements) == 22 or len(merged_elements) == 23 or len(merged_elements) == 24:
                #     logger.info(f"text1: {text1} text2: {text2} x1: {x1} x2: {x2} w1: {w1} w2: {w2} h1: {h1} h2: {h2} y1: {y1} y2: {y2}")
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

    def merge_overlapping_boxes(self, text_elements: List[Dict[str, int]]) -> List[Dict[str, int]]:
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
                # Check if right edge of box1 overlaps left edge of box2 or vice versa
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
                            # new_h = max(y1 + h1, y2 + h2) - new_y
                            new_h = min(y1 + h1, y2 + h2) -new_y
                            new_text = text1 + ' ' + text2

                            # Update elem1
                            elem1 = {'text': new_text, 'x': new_x, 'y': new_y, 'width': new_w, 'height': new_h}
                            used_indices.add(j)

            merged_elements.append(elem1)
            used_indices.add(i)

        return merged_elements

    def draw_boxes(self,name:str, screenshot: bytes, merged_elements: List[Dict[str, int]]) -> None:
        # Convert screenshot to PIL Image
        image = Image.open(io.BytesIO(screenshot))
        
        # Convert to OpenCV format for drawing
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Draw merged bounding boxes
        for i, elem in enumerate(merged_elements):
            x, y, w, h = elem['x'], elem['y'], elem['width'], elem['height']
            text = elem['text']
            
            # Draw bounding box
            padding_up = 0
            padding_side = 0
            box_thickness = 1
            box_color = (0, 0, 255)  # Red in BGR
            cv2.rectangle(cv_image, 
                        (x - padding_side, y - padding_up), 
                        (x + w + padding_side, y + h + padding_up), 
                        box_color, 
                        box_thickness)
            
            # if i == 23 or i == 24:
            #     if name == "merged_close":
            #       logger.info(f"text: {text} x: {x} y: {y} w: {w} h: {h} i: {i} ")
            # Put text
            font_size = 0.3
            font_weight = 1  # Ensure thickness is an integer
            # Draw text with white background for better visibility
            text_size = cv2.getTextSize(str(i), cv2.FONT_HERSHEY_SIMPLEX, font_size, 1)[0]
            cv2.rectangle(cv_image, (x-2, y-text_size[1]-8), (x+text_size[0]+2, y-2), (0,0,0), -1)
            cv2.putText(cv_image, str(i), (x, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, font_size, (255,255,255), font_weight)
        # Save merged annotated image
        print(f'screenshots/{name}_screenshot.png')
        cv2.imwrite(f'screenshots/{name}_screenshot.png', cv_image)



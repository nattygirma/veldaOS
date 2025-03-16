import cv2
import numpy as np
from datetime import datetime
import os

class Screenshot:
    def __init__(self):
        self.screenshots_dir = "screenshots"
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def save_screenshot(self, image, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        filepath = os.path.join(self.screenshots_dir, filename)
        cv2.imwrite(filepath, image)
        return filepath 
import pyautogui
import keyboard
import mouse
import numpy as np
import cv2
from PIL import Image
import io
from typing import Tuple, Optional
from loguru import logger
import time

class OSInteraction:
    """Handles OS-level interactions like screenshots, clicks, and keyboard input."""
    
    def __init__(self):
        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> bytes:
        """Take a screenshot of the screen or a specific region."""
        try:
            screenshot = pyautogui.screenshot(region=region)
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            raise
    
    def click(self, x: int, y: int, button: str = 'left', double: bool = False) -> bool:
        """Click at the specified coordinates."""
        try:
            if double:
                pyautogui.doubleClick(x, y, button=button)
            else:
                pyautogui.click(x, y, button=button)
            return True
        except Exception as e:
            logger.error(f"Failed to click at ({x}, {y}): {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.1) -> bool:
        """Type text with specified interval between keystrokes."""
        try:
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """Press a single key."""
        try:
            keyboard.press_and_release(key)
            return True
        except Exception as e:
            logger.error(f"Failed to press key {key}: {e}")
            return False
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """Move mouse to specified coordinates."""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            logger.error(f"Failed to move mouse to ({x}, {y}): {e}")
            return False
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        return pyautogui.position()
    
    def find_on_screen(self, template: bytes, confidence: float = 0.9) -> Optional[Tuple[int, int, int, int]]:
        """Find a template image on screen and return its location."""
        try:
            # Convert template bytes to numpy array
            template_img = Image.open(io.BytesIO(template))
            template_np = np.array(template_img)
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            
            # Convert to grayscale
            template_gray = cv2.cvtColor(template_np, cv2.COLOR_RGB2GRAY)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
            
            # Template matching
            result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                h, w = template_gray.shape
                return (max_loc[0], max_loc[1], w, h)
            return None
        except Exception as e:
            logger.error(f"Failed to find template on screen: {e}")
            return None
    
    def wait(self, seconds: float) -> None:
        """Wait for specified number of seconds."""
        time.sleep(seconds) 
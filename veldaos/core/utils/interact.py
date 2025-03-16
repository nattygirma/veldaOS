import pyautogui
import time

class Interact:
    def __init__(self):
        # Configure PyAutoGUI settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 1.0

    def click(self, x: int, y: int):
        """Click at the specified coordinates."""
        try:
            pyautogui.click(x, y)
            return True
        except Exception as e:
            print(f"Error clicking at coordinates ({x}, {y}): {str(e)}")
            return False

    def type_text(self, text: str):
        """Type the specified text."""
        try:
            pyautogui.typewrite(text)
            return True
        except Exception as e:
            print(f"Error typing text: {str(e)}")
            return False

    def press_key(self, key: str):
        """Press a specific key."""
        try:
            pyautogui.press(key)
            return True
        except Exception as e:
            print(f"Error pressing key {key}: {str(e)}")
            return False

    def move_to(self, x: int, y: int):
        """Move the mouse to the specified coordinates."""
        try:
            pyautogui.moveTo(x, y)
            return True
        except Exception as e:
            print(f"Error moving to coordinates ({x}, {y}): {str(e)}")
            return False 
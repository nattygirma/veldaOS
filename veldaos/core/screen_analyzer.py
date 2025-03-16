from typing import Dict, List, Tuple, Optional
from loguru import logger
from .utils.screenshot import Screenshot
from .utils.pytesseractocr import PyTesseractOCR
from .utils.system_prompt import SystemPrompt
from .utils.callLLM import CallLLM
from .utils.interact import Interact

class ScreenAnalyzer:
    """Analyzes screen content using OCR and LangChain for action determination."""
    
    def __init__(self, openai_api_key: str):
        self.screenshot_handler = Screenshot()
        self.ocr_handler = PyTesseractOCR()
        self.system_prompt = SystemPrompt().get_prompt()
        self.llm_handler = CallLLM(api_key=openai_api_key)
        self.interact_handler = Interact()
    
    def analyze_screenshot(self, screenshot: bytes, prompt: str) -> Dict:
        """
        Analyze screenshot using OCR and determine action using LLM.
        
        Args:
            screenshot: Screenshot image bytes
            prompt: User's desired action
            
        Returns:
            Dict containing action details
        """
        try:
            # Perform OCR
            text_elements = self.ocr_handler.perform_ocr(screenshot)
            
            # Get LLM response
            response = self.llm_handler.get_response(self.system_prompt, screenshot)
            
            # Parse and validate response
            action = self._parse_llm_response(response['content'])
            
            # Perform action
            action = self.interact_handler.perform_action(action, text_elements)
            
            return action
        except Exception as e:
            logger.error(f"Error analyzing screenshot: {e}")
            raise
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response into structured action format."""
        try:
            # Extract JSON from response
            import json
            import re
            
            # Find JSON-like structure in response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                action = json.loads(json_match.group())
                return action
            else:
                raise ValueError("No valid action format found in response")
                
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
            raise
    

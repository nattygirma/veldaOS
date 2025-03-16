import base64
from typing import List, Dict
import cv2
import numpy as np
from PIL import Image
import io
from openai import OpenAI

class CallLLM:
    def __init__(self, api_key: str, model: str = "gpt-4-vision-preview"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def get_response(self, prompt: str, screenshot: bytes) -> Dict:
        try:
            # Convert screenshot to base64
            image_base64 = base64.b64encode(screenshot).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": "User's Goal: What element should be interacted with to achieve this goal?"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]}
                ]
            )
            
            return response.choices[0].message
            
        except Exception as e:
            raise Exception(f"Error getting LLM response: {str(e)}")

    def prepare_image(self, image_path: str) -> str:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image at {image_path}")

        # Encode image to base64
        _, buffer = cv2.imencode('.png', image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return f"data:image/png;base64,{image_base64}"

    def analyze_screenshot(self, image_path: str, system_prompt: str, user_goal: str) -> str:
        try:
            image_data = self.prepare_image(image_path)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": f"User's Goal: {user_goal}"},
                        {"type": "image_url", "image_url": {"url": image_data}}
                    ]}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analyzing screenshot: {str(e)}" 
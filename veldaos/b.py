import os
import openai
import cv2
from typing import List, Dict
import base64

print(os.getenv("OPENAI_API_KEY"))

def get_response(image: bytes):
    if image is None:
        print("Failed to read the image. Please check the file path.")
        return

    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks."},
            {"role": "user", "content": [
                {"type": "text", "text": "User's Goal: What element should be interacted with to achieve this goal?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image).decode()}"}}
            ]}
        ]
    )

    print(completion.choices[0].message)

# Print the current working directory
print("Current working directory:", os.getcwd())

# Attempt to read the image
image = cv2.imread("../screenshots/merged_close_screenshot.png")

# Call the function
get_response(image)


 

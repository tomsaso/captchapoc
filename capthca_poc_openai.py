import openai
import base64

# It's not safe to hardcode API keys in your code. Consider using environment variables or a secure vault.
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")  # Fetch the API key from an environment variable

if not API_KEY:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

image_path = "image2.jpg"
openai.api_key = API_KEY

try:
    with open(image_path, "rb") as image_file:
        # Encode the image in base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
except FileNotFoundError:
    raise FileNotFoundError(f"Image file not found at path: {image_path}")

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "This image is split into 4x4 parts. Can you give me the coordinates of the parts where you see traffic lights? \
                 please provide only the coordinates in (row,column) format, no other text."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=300
)

print(response.choices[0].message.content)

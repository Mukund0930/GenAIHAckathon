import os
import openai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
except Exception as e:
    print(f"Error configuring OpenAI: {e}")


def generate_image_with_dalle(prompt):
    """
    Generates an image using OpenAI's DALL-E 3 model.
    """
    if not openai.api_key:
        return "Error: OpenAI API key not configured."
        
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="hd"
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return f"An error occurred with the OpenAI API: {e}"
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from google.cloud import translate_v2 as translate

# Load environment variables from the .env file
load_dotenv()

# --- Section 1: Configure API Clients ---

# Configure the Gemini API client
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"--- 🚨 CRITICAL ERROR CONFIGURING GOOGLE AI ---")
    print(f"Could not configure the Gemini API. Check your .env file and GOOGLE_API_KEY. Details: {e}")
    gemini_model = None

# Configure the Cloud Translation API client
try:
    # The translate library automatically finds your credentials
    # It works with the same API key setup or Application Default Credentials
    translate_client = translate.Client()
except Exception as e:
    print(f"--- 🚨 CRITICAL ERROR CONFIGURING TRANSLATE CLIENT ---")
    print(f"Could not initialize the Translation client. Ensure the API is enabled. Details: {e}")
    translate_client = None


# --- Section 2: Translation Function ---

def translate_text(text: str, target_language: str) -> str:
    """Translates text into the target language using Google Cloud Translate."""
    # Return original text if the client failed to initialize or there's no text
    if not translate_client or not text:
        return text
    # Avoid unnecessary API calls if the target is English (or the source language)
    if target_language == 'en':
        return text
    try:
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        print(f"Translation Error: {e}")
        return text # Fallback to original text if translation fails


# --- Section 3: Gemini API Functions ---

def generate_product_descriptions(artisan_context, product_name, materials):
    """Generates three distinct product description styles using Gemini."""
    if not gemini_model:
        return {"error": "Google AI model not configured. Please check your API key."}

    try:
        prompt = f"""
        You are an expert e-commerce copywriter specializing in handmade artisanal crafts.
        Your task is to generate three distinct product descriptions for a new listing.

        **Primary Context: The Artisan's Story (This is the most important information)**
        ---
        {artisan_context}
        ---

        **Product Details:**
        - Product Name: {product_name}
        - Materials Used: {materials}

        **Instructions:**
        You MUST respond with ONLY a valid JSON object. Do not include any other text or markdown formatting like ```json. The JSON object must have these exact keys: "story_driven", "bullet_points", "social_media_caption". The value for "bullet_points" must be an array of strings.
        """
        
        response = gemini_model.generate_content(prompt)
        
        # Robustly find and extract the JSON object from the response text
        text = response.text
        start_index = text.find('{')
        end_index = text.rfind('}') + 1
        
        if start_index == -1 or end_index == 0:
            raise ValueError("Could not find a valid JSON object in the AI response.")
            
        cleaned_json_string = text[start_index:end_index]
        return json.loads(cleaned_json_string)
        
    except Exception as e:
        return {"error": f"An error occurred with the Gemini API or parsing its response: {e}"}


def answer_customer_query(artisan_context, product_details, question):
    """Answers a customer query using the artisan and product info as its only knowledge base."""
    if not gemini_model:
        return "Error: Google AI model not configured."

    try:
        prompt = f"""
        You are a friendly and helpful customer service bot for an artisan marketplace.
        Your name is Sahayak Bot. You have one critical rule: **You must only answer questions using the information provided below.** Do not make up any information, prices, or policies. If the answer is not in the context, politely state that you can provide details about the craft's origin and the artisan's story.

        **Source of Truth: Artisan's Story**
        ---
        {artisan_context}
        ---

        **Source of Truth: Product Details**
        ---
        {product_details}
        ---

        **Customer's Question:**
        "{question}"

        Now, answer the customer's question based *only* on the provided information.
        """
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred with the Gemini API: {e}"
    

def generate_social_media_plan(artisan_context, product_name, campaign_goal):
    """Generates a complete 3-day social media plan using Gemini."""
    if not gemini_model:
        return {"error": "Google AI model not configured."}
    try:
        prompt = f"""
        You are a professional social media strategist who specializes in helping independent artisans.
        Your task is to create a 3-day social media content plan to help an artisan achieve their goal.

        **Primary Context: The Artisan's Story**
        ---
        {artisan_context}
        ---

        **Product to Feature:**
        - Product Name: {product_name}

        **Campaign Goal:**
        - {campaign_goal}

        **Instructions:**
        You MUST respond with ONLY a valid JSON object. The object must have a key "plan_title" and a key "posts".
        The "posts" key must contain a list of exactly 3 JSON objects.
        Each post object must have these three keys: "day_title", "suggested_image", and "caption".
        - "day_title": A short, catchy title for the day's post (e.g., "Day 1: The Teaser").
        - "suggested_image": A brief description of the type of photo the artisan should use.
        - "caption": The full, ready-to-use caption, complete with engaging text, emojis, and 3-5 relevant hashtags.
        """
        
        response = gemini_model.generate_content(prompt)
        text = response.text
        start = text.find('{')
        end = text.rfind('}') + 1
        cleaned_json_string = text[start:end]
        return json.loads(cleaned_json_string)
    except Exception as e:
        return {"error": f"An error occurred with the Gemini API or parsing the response: {e}"}
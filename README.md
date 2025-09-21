KalaKriti AI: An AI-Powered E-commerce Platform for Local Artisans
🌟 Vision
Indian artisans and craftsmen possess incredible traditional skills but often struggle to connect with modern digital audiences. KalaKriti AI is a prototype e-commerce platform designed to bridge this gap. It leverages the power of Google's Generative AI to provide local artisans with intelligent tools to market their craft, tell their unique stories, and automate their digital workflow, ultimately expanding their reach and preserving valuable cultural heritage.

This project was developed as a creative solution to empower artisans in the digital marketplace.

✨ Core Features
This platform is a multi-page Streamlit application that serves both customers and artisans.

🛍️ Public E-commerce Marketplace: A beautiful, searchable storefront where customers can discover and view products from all registered artisans.

👤 Secure Artisan Dashboard: A password-protected area where artisans can register, log in, and manage their profile.

✍️ AI-Powered Product Listing: Artisans provide basic product details, and the AI (powered by Google Gemini) generates multiple compelling, ready-to-use description suggestions (story-driven, bullet points, social media captions). The AI always uses the artisan's personal story as the core context for authentic results.

🤖 Automated Assistant Bot: A context-aware chatbot that artisans can use to see how an AI would answer customer questions. The bot uses the artisan's story and product details as its only source of truth, ensuring accurate and helpful responses.

🗓️ AI Post Planner: A social media strategist tool that generates a complete 3-day content plan based on a specific campaign goal, helping artisans automate their marketing workflow.

🌐 Multilingual Support: The entire platform can be translated into Hindi and Gujarati with a single click, powered by the Google Cloud Translate API.

🛠️ Tech Stack
Frontend: Streamlit

Backend & Core Logic: Python

Generative AI (Text): Google Gemini API (gemini-1.5-flash-latest)

Translation: Google Cloud Translate API

Database: Simple local database.json file (for this prototype)

Security: Python's hashlib for secure password hashing.

🚀 Getting Started
Follow these steps to set up and run the project on your local machine.

Prerequisites

Python 3.8+

Git

Google Cloud SDK (gcloud CLI)

1. Clone the Repository

git clone [https://github.com/Mukund0930/GenAIHAckathon.git](https://github.com/Mukund0930/GenAIHAckathon.git)
cd GenAIHAckathon

2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment.

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies

Install all the required Python libraries.

pip install -r requirements.txt

4. Set Up API Keys & Credentials

You need to provide your Google API key for Gemini and authenticate for the Translation API.

a. Create a .env file:
Create a file named .env in the root of the project directory and add your Google API key to it. You can get a key from the Google AI Studio.

GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"

b. Authenticate for Google Cloud Translate:
The Translation API requires more secure authentication. Run this command in your terminal and follow the instructions to log in with your Google account.

gcloud auth application-default login

c. Enable the Cloud Translation API:
Make sure you have enabled the "Cloud Translation API" in your Google Cloud project console.

5. Run the Streamlit App

Once the setup is complete, run the application from your terminal.

streamlit run 1_🏠_Marketplace_Home.py

Your web browser should open with the application running!

📖 How to Use
Register as an Artisan: Navigate to the "Artisan Dashboard" from the sidebar and choose the "Register" option. Create a unique username and password.

Login: Log in with your new credentials.

Create Your Profile: Fill out your name, craft type, and most importantly, "Your Story". This story is the context the AI will use for all generations.

Add a Product: Go to the "Add New Product" page, fill in the details, and click "Generate AI Suggestions". Use the suggestions to populate the final descriptions.

Explore Other Tools: Test the "Automated Assistant Bot" and the "AI Post Planner" to see how the AI uses your profile to help you.

Translate the Site: Use the language selector in the sidebar to view the platform in Hindi or Gujarati.

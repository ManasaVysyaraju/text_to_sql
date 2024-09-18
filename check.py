from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load all the environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to list available models
def list_available_models():
    models_generator = genai.list_models()
    models_list = list(models_generator)  # Convert generator to list
    return models_list

# Check available models
models = list_available_models()
print("Available Models:")
for model in models:
    print(model)


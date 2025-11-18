import os
from dotenv import load_dotenv
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features, EntitiesOptions, CategoriesOptions, SentimentOptions, KeywordsOptions
)

# --- CONFIGURATION ---
# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
SERVICE_URL = os.getenv("IBM_SERVICE_URL")
NLU_VERSION = "2022-04-07"
# ---------------------

# --- Service Initializer ---
nlu_service = None

if not API_KEY or not SERVICE_URL:
    print("Error: IBM_API_KEY or IBM_SERVICE_URL not found in .env file.")
    print("Please create a .env file and add your IBM credentials.")
else:
    try:
        # --- Authentication ---
        authenticator = IAMAuthenticator(API_KEY)
        nlu_service = NaturalLanguageUnderstandingV1(
            version=NLU_VERSION,
            authenticator=authenticator
        )
        nlu_service.set_service_url(SERVICE_URL)
        print("IBM Watson NLU service initialized successfully from .env file.")

    except Exception as auth_error:
        print(f"Error initializing IBM Watson NLU service: {auth_error}")
        nlu_service = None

# --- Define Analysis Features ---
analysis_features = Features(
    entities=EntitiesOptions(
        limit=50,
        mentions=True
    ),
    categories=CategoriesOptions(
        limit=5,
        model='ibm-generic_taxonomy'
    ),
    sentiment=SentimentOptions(
        document=True
    ),
    keywords=KeywordsOptions(
        limit=20,
        sentiment=False,
        emotion=False
    )
)

def analyze_legal_text(text_content):
    """
    Analyzes the provided text using the configured IBM Watson NLU service.
    """
    if nlu_service is None:
        print("NLU service is not initialized. Analysis cancelled.")
        return None
        
    if not text_content:
        print("No text content provided to analyze. Skipping.")
        return None

    try:
        response = nlu_service.analyze(
            text=text_content,
            features=analysis_features,
            language='en'
        ).get_result()
        
        print("Analysis successful.")
        return response
        
    except Exception as e:
        print(f"Error during NLU analysis: {e}")
        return None
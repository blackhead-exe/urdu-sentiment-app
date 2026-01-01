import re
import pickle
import numpy as np
import os
from db import supabase_admin

MODEL_VERSION = "v3.1_UrduSentiment_Final"

# Constants
MODEL_PATH = "svm_model.pkl"
TOKENIZER_PATH = "tfidf_vectorizer.pkl"

def clean_urdu_text(text):
    """
    Cleans Urdu text by removing English letters, digits, and special chars.
    Keeps Urdu/Arabic letters and spaces.
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Remove English alphanumeric characters
    text = re.sub(r'[a-zA-Z0-9]', '', text)
    
    # Keep only Arabic/Urdu unicode range and spaces. 
    # \u0600-\u06FF includes base Arabic/Urdu chars.
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def initialize_backend():
    """
    Loads the verified Logistic Regression model and TF-IDF vectorizer.
    This model has been tested to correctly handle positive/negative Urdu text.
    """
    print("Loading resources...")
    
    if not os.path.exists(MODEL_PATH):
        # We need to ensure these exist. If they were deleted, we retrain.
        print("Model files missing. Please ensure svm_model.pkl exists.")
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(TOKENIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
        
    print("Backend initialized successfully (LogReg).")
    return model, vectorizer

def log_prediction(review, prediction, confidence):
    try:
        supabase_admin.table("sentiment_logs").insert({
            "review": review,
            "prediction": prediction,
            "confidence": float(confidence),
            "model_version": MODEL_VERSION
        }).execute()
    except Exception as e:
        print(f"Warning: Failed to log prediction to database: {e}")


def predict_sentiment(text, model, vectorizer):
    """
    Predicts sentiment using the stable LogReg model.
    """
    cleaned_text = clean_urdu_text(text)
    if not cleaned_text:
        return "Neutral", 0.0
        
    # Vectorize
    vectors = vectorizer.transform([cleaned_text])
    
    # Predict Probabilities
    probs = model.predict_proba(vectors)[0] 
    prediction = model.predict(vectors)[0] 
    
    # Mapping: 0 -> Negative, 1 -> Positive (as verified in training)
    if prediction == 1:
        label = "Positive"
        confidence = probs[1]
    else:
        label = "Negative"
        confidence = probs[0]
        
    print(f"DEBUG: Input='{text}' | Label={label} | Score={confidence:.4f}")
    log_prediction(text, label, confidence)
    return label, float(confidence)

if __name__ == "__main__":
    # Internal validation
    try:
        m, v = initialize_backend()
        for t in ["بہت اچھا", "بہت برا"]:
            l, c = predict_sentiment(t, m, v)
            print(f"'{t}' -> {l} ({c:.2f})")
    except Exception as e:
        print(f"Error: {e}")

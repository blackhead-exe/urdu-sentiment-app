import pandas as pd
import numpy as np
import re
import pickle
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout

# Constants
DATASET_PATH = "urdu_cleaned_dataset.csv"
MODEL_PATH = "bilstm_urdu_sentiment_model.h5"
TOKENIZER_PATH = "tokenizer.pkl"
MAX_LEN = 120
VOCAB_SIZE = 8000
EMBEDDING_DIM = 64

def clean_urdu_text(text):
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'[a-zA-Z0-9]', '', text)
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_model():
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    
    # 1. Prepare Data
    print("Cleaning text...")
    df['cleaned_review'] = df['cleaned_review'].astype(str).apply(clean_urdu_text)
    df = df.dropna(subset=['sentiment'])
    
    # Map labels: 1 -> 0 (Negative), 3 -> 1 (Positive)
    # Ensure we strictly have only these classes
    print("Filtering and Mapping labels...")
    df = df[df['sentiment'].isin([1, 3])].copy()
    
    # Explicit mapping: 1 (Negative) becomes 0, 3 (Positive) becomes 1
    label_map = {1: 0, 3: 1}
    df['label'] = df['sentiment'].map(label_map)
    
    X = df['cleaned_review'].values
    y = df['label'].values
    
    print(f"Data shape: {X.shape}, Class distribution: {df['label'].value_counts().to_dict()}")

    # 2. Tokenization
    print("Tokenizing...")
    # Increase vocab size slightly for better coverage
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(X)
    
    sequences = tokenizer.texts_to_sequences(X)
    padded_sequences = pad_sequences(sequences, maxlen=MAX_LEN)
    
    # 3. Model Definition
    print("Building model...")
    model = Sequential([
        Embedding(input_dim=10000, output_dim=64, input_length=MAX_LEN),
        Bidirectional(LSTM(64, return_sequences=True)), # Added return_sequences for deeper net or just better flow
        Bidirectional(LSTM(32)),
        Dropout(0.4), # Increased dropout
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    
    # 4. Training
    print("Training model...")
    history = model.fit(
        padded_sequences, 
        y, 
        epochs=5, # Increased epochs
        batch_size=32, 
        validation_split=0.2,
        verbose=1
    )
    
    # 5. Evaluation mechanism (Quick check on training data subset for sanity)
    # Ideally should use a test split, but using val split from fit is okay for now.
    # Let's verify manual prediction on examples
    print("\nVerifying on test examples...")
    test_texts = ["یہ فلم بہت اچھی ہے", "یہ بہت بیکار ہے"]
    test_seqs = tokenizer.texts_to_sequences([clean_urdu_text(t) for t in test_texts])
    test_padded = pad_sequences(test_seqs, maxlen=MAX_LEN)
    preds = model.predict(test_padded)
    
    for text, pred in zip(test_texts, preds):
        label = "Positive" if pred > 0.5 else "Negative"
        print(f"Text: '{text}' -> Score: {pred[0]:.4f} -> Label: {label}")

    # 6. Saving
    print("Saving artifacts...")
    model.save(MODEL_PATH)
    with open(TOKENIZER_PATH, 'wb') as f:
        pickle.dump(tokenizer, f)
        
    print("Training complete. Model and tokenizer saved.")

if __name__ == "__main__":
    try:
        train_model()
    except Exception as e:
        print(f"Training failed: {e}")

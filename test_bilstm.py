
import backend
import os
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    print("Initializing backend...")
    model, tokenizer = backend.initialize_backend()
    
    test_cases = [
        "یہ فلم بہت اچھی ہے", 
        "یہ بالکل فضول ہے"
    ]
    
    for text in test_cases:
        label, score = backend.predict_sentiment(text, model, tokenizer)
        # Use simple ASCII for output to avoid font issues if needed, but utf-8 should work now
        print(f"Text: {text} -> Label: {label}, Score: {score:.4f}")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")

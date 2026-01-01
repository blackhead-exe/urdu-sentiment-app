import pandas as pd
import plotly.express as px
import os

DATASET_PATH = "urdu_cleaned_dataset.csv"

print(f"Testing CSV file: {DATASET_PATH}")
if os.path.exists(DATASET_PATH):
    try:
        # Try reading with utf-8
        df = pd.read_csv(DATASET_PATH, encoding='utf-8')
        print("Successfully read CSV with utf-8.")
        print("Columns:", df.columns.tolist())
        print("Head (2 rows):")
        print(df.head(2))
        print(f"Total rows: {len(df)}")
    except Exception as e:
        print(f"Failed to read with utf-8: {e}")
        try:
            # Fallback
            df = pd.read_csv(DATASET_PATH, encoding='utf-16')
            print("Successfully read CSV with utf-16.")
        except Exception as e2:
            print(f"Failed to read with utf-16: {e2}")

    try:
        print("\nTesting Plotly import...")
        fig = px.bar(x=[1, 2, 3], y=[1, 3, 2])
        print("Plotly figure created successfully.")
    except Exception as e:
        print(f"Plotly Error: {e}")

else:
    print("File not found.")

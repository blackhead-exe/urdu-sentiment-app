import streamlit as st
try:
    print(f"Streamlit version: {st.__version__}")
    if hasattr(st, "navigation"):
        print("st.navigation is available")
    else:
        print("st.navigation is NOT available")
except Exception as e:
    print(f"Error checking streamlit: {e}")

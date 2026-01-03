import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from db import supabase_public
from auth import login, signup, logout


# -------- Session state --------
# User and Messages are now initialized in app.py
if "user" not in st.session_state:
    st.session_state.user = None

# Restore session from Supabase client if available (fixes refresh logout)
if st.session_state.user is None:
    session = supabase_public.auth.get_session()
    if session:
        st.session_state.user = session.user

# -------- Login / Signup UI --------
def auth_ui():
    if st.sidebar.button("🔙 Back to Chat"):
        st.switch_page("pages/chat.py")
    st.title("Admin Login")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            try:
                res = login(email, password)
                st.session_state.user = res.user
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")

    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            try:
                signup(email, password)
                st.success("Signup successful. Please login.")
            except:
                st.error("Signup failed")

# -------- Dashboard --------
def dashboard():
    st.sidebar.button("Log Out", on_click=logout)
    if st.sidebar.button("🔙 Back to Chat"):
        st.switch_page("pages/chat.py")

    st.title("Sentiment Admin Dashboard")

    @st.cache_data(ttl=30)
    def load_logs():
        data = supabase_public.table("sentiment_logs").select("*").order("created_at", desc=True).limit(1000).execute().data
        return pd.DataFrame(data)

    df = load_logs()

    st.metric("Total Logs", len(df))
    st.metric("Positive", (df["prediction"] == "Positive").sum())
    st.metric("Negative", (df["prediction"] == "Negative").sum())

    st.dataframe(df, use_container_width=True)

# -------- Routing --------
if st.session_state.user is None:
    auth_ui()
else:
    dashboard()

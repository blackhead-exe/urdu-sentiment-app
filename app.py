import streamlit as st
from db import supabase_public

# --- 0. Set Global Config (Must be first) ---
if "user" not in st.session_state:
    st.session_state.user = None

# Restore session from Supabase client if available (fixes refresh logout)
if st.session_state.user is None:
    try:
        session = supabase_public.auth.get_session()
        if session:
            st.session_state.user = session.user
    except:
        pass

admin_title = "Admin"
if st.session_state.user:
    admin_title = st.session_state.user.email

st.set_page_config(
    page_title=f"UrduAI - {admin_title if st.session_state.user else 'Chat'}",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. Global Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}  # {chat_id: {"title": str, "messages": list}}
    
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
    
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 0

# --- 2. Navigation Setup ---
# Using file-based pages for robust switching
pg_chat = st.Page("pages/chat.py", title="Chat", icon="🤖", default=True)
pg_admin = st.Page("pages/admin.py", title="Admin", icon="👤")

pg = st.navigation([pg_chat, pg_admin], position="hidden")

# --- 3. Global CSS ---
st.markdown("""
<style>
    /* General button styling */
    .stButton>button {
        border-radius: 8px !important;
        width: 100% !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    
    /* New Chat button */
    button[key="new_chat_btn"] {
        background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    button[key="new_chat_btn"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Chat history buttons */
    div[data-testid="column"]:first-child .stButton>button {
        background-color: transparent !important;
        color: white !important;
        text-align: left !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    div[data-testid="column"]:first-child .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Delete buttons */
    div[data-testid="column"]:last-child .stButton>button {
        background-color: transparent !important;
        color: #dc3545 !important;
    }
    
    /* User profile button */
    button[key="user_profile_btn"], button[key="admin_login_btn"] {
        background-color: transparent !important;
        color: white !important;
        text-align: left !important;
    }
    
    button[key="user_profile_btn"]:hover, button[key="admin_login_btn"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Search input */
    div[data-testid="stTextInput"] input {
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Hide branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

pg.run()

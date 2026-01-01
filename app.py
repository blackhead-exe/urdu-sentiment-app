import streamlit as st
import backend
import time

# Page config
st.set_page_config(
    page_title="UrduAI - Sentiment Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Optional) ---
st.markdown("""
<style>
    /* Premium Button Look */
    .stButton>button {
        border-radius: 8px !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)


# Main Header (Render this FIRST so user sees something)
# We can use a placeholder or just standard markdown
st.title("🤖 UrduAI Chat")

# Initialize backend
@st.cache_resource
def load_stable_model():
    return backend.initialize_backend()

# Load with visual feedback
placeholder = st.empty()
try:
    with placeholder.container():
        st.info("🧠 Initializing AI Model... Please wait.")
        with st.spinner("Loading Stable Sentiment Model..."):
            model, vectorizer = load_stable_model()
    placeholder.empty() # Clear loading message on success
except Exception as e:
    st.error(f"Failed to load backend: {e}")
    st.stop()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown("### New Chat")
    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("### History")
    st.caption("Today")
    if len(st.session_state.messages) > 0:
        st.text(f"📝 {st.session_state.messages[0]['content'][:15]}...")
    else:
        st.caption("No history yet.")
        
    st.markdown("---")
    st.caption("Model: **UrduSentiment PRO v3.1 (Stable)**")
    st.caption("Admin Access available in sidebar.")

# Header (minimal)
# st.markdown("#### Urdu Sentiment GPT") 

# Display Chat History
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        avatar = "👤" # Or path to user icon
        with st.chat_message("user", avatar=avatar):
            st.markdown(content)
    else:
        avatar = "🤖" # Or ChatGPT logo
        with st.chat_message("assistant", avatar=avatar):
            st.markdown(content)

# Chat Input
if prompt := st.chat_input("Send a message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 1. Processing State
        with st.spinner("Thinking..."):
            # time.sleep(0.5) # Simulate network delay
            label, conf = backend.predict_sentiment(prompt, model, vectorizer)
        
        # 2. Construct Response
        if label == "Positive":
            sentiment_emoji = "😊"
            color = "green"
        else:
            sentiment_emoji = "😠"
            color = "red"
            
        # Creating a structured markdown response
        response_md = f"""
**Sentiment Analysis Result**

- **Input**: *"{prompt}"*
- **Sentiment**: <span style='color:{color}; font-weight:bold'>{label} {sentiment_emoji}</span>
- **Confidence**: `{conf*100:.1f}%`

---
If you need further analysis, feel free to ask!
        """
        
        # 3. Stream output (simulated)
        # ChatGPT usually streams tokens. We can simulate this locally for effect.
        
        # Pre-calc the static part or stream it char by char
        # For simplicity in 'replace_file_content', we just show it.
        # But let's add a small effect for the "ChatGPT feels"
        
        message_placeholder.markdown(response_md, unsafe_allow_html=True)
        
        # Save to history
        st.session_state.messages.append({"role": "assistant", "content": response_md})

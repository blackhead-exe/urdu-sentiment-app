import streamlit as st
import backend
import time
from db import supabase_public

# --- Helper Functions for Chat Management ---
def create_new_chat():
    """Creates a new chat session"""
    # Save current chat if it has messages
    if st.session_state.messages and st.session_state.current_chat_id:
        save_current_chat()
    
    # Create new chat
    st.session_state.chat_counter += 1
    new_chat_id = f"chat_{st.session_state.chat_counter}"
    st.session_state.current_chat_id = new_chat_id
    st.session_state.messages = []
    
def save_current_chat():
    """Saves the current chat to history"""
    if st.session_state.current_chat_id and st.session_state.messages:
        # Generate title from first user message
        title = "New Chat"
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                title = msg["content"][:30] + ("..." if len(msg["content"]) > 30 else "")
                break
        
        st.session_state.chat_history[st.session_state.current_chat_id] = {
            "title": title,
            "messages": st.session_state.messages.copy()
        }

def load_chat(chat_id):
    """Loads a chat from history"""
    # Save current chat first
    if st.session_state.messages and st.session_state.current_chat_id:
        save_current_chat()
    
    # Load selected chat
    if chat_id in st.session_state.chat_history:
        st.session_state.current_chat_id = chat_id
        st.session_state.messages = st.session_state.chat_history[chat_id]["messages"].copy()

# --- Page Logic ---
def chat_page():
    # Page config (Inner title)
    st.title("Urdu Chat Analyzer")

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
    
    # Initialize first chat if needed
    if st.session_state.current_chat_id is None:
        create_new_chat()


    # Sidebar Tools (ChatGPT-style layout)
    with st.sidebar:
        # 1. New Chat Button at the top
        if st.button("✏️ New chat", use_container_width=True, key="new_chat_btn"):
            create_new_chat()
            st.rerun()
        
        # 2. Search chats input
        if "chat_search_query" not in st.session_state:
            st.session_state.chat_search_query = ""
        
        search_query = st.text_input(
            "Search", 
            value=st.session_state.chat_search_query,
            placeholder="Search chats",
            key="chat_search_input",
            label_visibility="collapsed"
        )
        st.session_state.chat_search_query = search_query
        
        st.markdown("---")
        
        # 3. Chat History Section
        st.markdown("**Your chats**")
        
        # Display saved chats
        if st.session_state.chat_history:
            # Sort chats by ID (most recent first)
            sorted_chats = sorted(
                st.session_state.chat_history.items(), 
                key=lambda x: int(x[0].split('_')[1]), 
                reverse=True
            )
            
            # Filter chats based on search query
            if search_query:
                filtered_chats = [
                    (chat_id, chat_data) for chat_id, chat_data in sorted_chats
                    if search_query.lower() in chat_data['title'].lower()
                ]
            else:
                filtered_chats = sorted_chats
            
            if filtered_chats:
                for chat_id, chat_data in filtered_chats:
                    col1, col2 = st.columns([5, 1])
                    
                    with col1:
                        # Create a button for each chat
                        is_current = chat_id == st.session_state.current_chat_id
                        button_label = chat_data['title']
                        
                        if st.button(button_label, key=f"load_{chat_id}", use_container_width=True):
                            load_chat(chat_id)
                            st.rerun()
                    
                    with col2:
                        # Delete button
                        if st.button("🗑️", key=f"del_{chat_id}"):
                            del st.session_state.chat_history[chat_id]
                            if st.session_state.current_chat_id == chat_id:
                                create_new_chat()
                            st.rerun()
            else:
                st.caption(f"No chats found matching '{search_query}'")
        else:
            st.caption("No chat history yet")
        
        # 4. Spacer to push user profile to bottom
        st.markdown("<div style='height: 100%; min-height: 200px;'></div>", unsafe_allow_html=True)
        
        # 5. User Profile at the very bottom (like ChatGPT)
        st.markdown("---")
        if st.session_state.user:
            user_email = st.session_state.user.email
            # Extract username from email (before @)
            username = user_email.split('@')[0] if '@' in user_email else user_email
            
            # Create user profile button with avatar
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"""
                <div style='
                    width: 32px; 
                    height: 32px; 
                    border-radius: 50%; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                '>
                    {username[0].upper()}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button(username, use_container_width=True, key="user_profile_btn"):
                    st.switch_page("pages/admin.py")
        else:
            if st.button("👤 Login", use_container_width=True, key="admin_login_btn"):
                st.switch_page("pages/admin.py")



    # Display Chat History
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            avatar = "👤"
            with st.chat_message("user", avatar=avatar):
                st.markdown(content)
        else:
            avatar = "🤖"
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
            
            # 1. Processing State
            with st.spinner("Thinking..."):
                label, conf = backend.predict_sentiment(prompt, model, vectorizer)
            
            # 2. Construct Response
            if label == "Positive":
                sentiment_emoji = "😊"
                color = "green"
            else:
                sentiment_emoji = "😠"
                color = "red"
                
            response_md = f"""
**Sentiment Analysis Result**

- **Input**: *"{prompt}"*
- **Sentiment**: <span style='color:{color}; font-weight:bold'>{label} {sentiment_emoji}</span>
- **Confidence**: `{conf*100:.1f}%`

---
If you need further analysis, feel free to ask!
            """
            
            message_placeholder.markdown(response_md, unsafe_allow_html=True)
            
            # Save to history
            st.session_state.messages.append({"role": "assistant", "content": response_md})
        
        # Auto-save current chat after message exchange
        save_current_chat()

# Run the page function
chat_page()

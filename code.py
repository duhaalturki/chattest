import streamlit as st
import requests

# Together AI API Key (Replace with your actual API key)
TOGETHER_API_KEY = "85b9952e2ec424e60e2be7e243963eb121dd91bb33f6b9afd8a9ee1d6a114e47"

# Function to get chatbot response
def get_response_from_together(messages):
    try:
        api_url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """
        You are a supportive and empathetic mental health assistant. Your job is to comfort users, validate their feelings, and gently encourage them to seek professional help when necessary.
        
        - Always respond in a warm and caring way.
        - Never dismiss the user's feelings.
        - Avoid generic answers—make each response unique and thoughtful.
        - If a user expresses suicidal thoughts, provide crisis resources instead of general reassurance.
        """

        
        data = {
            "model": "meta-llama/Llama-2-7b-chat-hf",  # ✅ Chat-focused model
            "messages": messages,
            "temperature": 0.8,
            "max_tokens": 200
        }
        
        response = requests.post(api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.error(f"Error: {response.status_code}, Message: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Apply Green Background with CSS
st.markdown(
    """
    <style>
      body {
        background-image: url('assests/green.png');
        background-size: cover;
        background-position: center;
        color: white;
    }
     .stApp {
        background-image: url('assests/green.png') !important;
        
        background-size: cover;
        background-position: center;
    }
    .stTextInput > div > div > input {
        background-color: white;
        color: black;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("💬 ZenMind - Mental Health Chatbot")
st.write("This chatbot provides support using a **free AI model from Together AI**.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Hello! How are you feeling today?"}]

# Display past messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get AI response
    response = get_response_from_together(st.session_state.messages)
    
    if response:
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

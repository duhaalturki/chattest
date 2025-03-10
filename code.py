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

# Apply custom CSS for background animation
st.markdown(
    """
    <style>
        @keyframes fadeInOut {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 0; }
        }
        .animated-text {
            position: fixed;
            width: 100%;
            text-align: center;
            top: 10%;
            font-size: 24px;
            color: white;
            font-weight: bold;
            opacity: 0;
            animation: fadeInOut 5s infinite;
        }
        body {
            background: linear-gradient(to bottom, #008000, #004d00);
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Positive words to animate
positive_messages = [
    "Don't worry, it's going to be alright!",
    "You're going to make it!",
    "You are strong and capable!",
    "Better days are ahead!"
]

# Display an animated positive message
st.markdown(f'<div class="animated-text">{random.choice(positive_messages)}</div>', unsafe_allow_html=True)
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

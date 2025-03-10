import streamlit as st
import requests

# Together AI API Key (Replace with your actual API key)
TOGETHER_API_KEY = "85b9952e2ec424e60e2be7e243963eb121dd91bb33f6b9afd8a9ee1d6a114e47"


# Function to get chatbot response
def get_response_from_together(prompt):
    try:
        api_url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",  # ✅ Updated to a valid model
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
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

# Streamlit UI
st.title("💬 Mental Health Chatbot")
st.write("This chatbot provides support using a **free AI model from Together AI**.")

# Get user input
user_input = st.text_input("How are you feeling today?")

if user_input:
    response = get_response_from_together(user_input)
    
    if response:
        st.write(response)

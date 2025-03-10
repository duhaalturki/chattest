import streamlit as st
import requests

# Function to get response from Mistral API
def get_mistral_response(prompt):
    try:
        # Mistral API URL (replace with the correct URL provided by Mistral)
        api_url = "https://api.mistral.ai/v1/generate"  # Example URL, confirm with Mistral's documentation
        
        headers = {
            "Authorization": f"Bearer {st.secrets['general']['mistral_api_key']}",  # Get API key from secrets.toml
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,  # The user input that the chatbot will respond to
            "max_tokens": 150  # Set maximum response length (optional)
        }

        # Sending POST request to Mistral API
        response = requests.post(api_url, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()['choices'][0]['text']  # Adjust this based on the actual API response format
        else:
            st.error(f"Error: {response.status_code}, Message: {response.json().get('error', {}).get('message', 'Unknown Error')}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit UI for chatbot
st.title("💬 Chatbot - Mental Health Support")
st.write("This is a simple chatbot powered by Mistral API, designed to provide mental health support.")

# Input from user
if prompt := st.text_input("Enter your message"):
    response = get_mistral_response(prompt)
    if response:
        st.write(response)

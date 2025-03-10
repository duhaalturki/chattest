import streamlit as st
import requests

# Function to get response from Mistral API
def get_mistral_response(prompt):
    try:
        api_url = "https://api.mistral.ai/v1/generate"  # Replace with actual Mistral API URL
        
        headers = {
            "Authorization": f"Bearer {st.secrets['general']['mistral_api_key']}",  # Access the API key securely
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "max_tokens": 150
        }

        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['text']  # Adjust based on Mistral's response format
        else:
            st.error(f"Error: {response.status_code}, Message: {response.json().get('error', {}).get('message', 'Unknown Error')}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Example usage in Streamlit
st.title("💬 Chatbot - Mental Health Support")
st.write("This is a chatbot powered by Mistral API for mental health support.")

if prompt := st.text_input("Enter your message"):
    response = get_mistral_response(prompt)
    if response:
        st.write(response)

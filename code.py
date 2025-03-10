import streamlit as st
import requests

# Directly define the Mistral API key here
mistral_api_key = "rqdW8BDnyzYFubXuNjew305C8pjUUCxH"  # Replace with your actual API key

# Function to get a response from Mistral API
def get_mistral_response(prompt):
    try:
        api_url = "https://api.mistral.ai/v1/generate"  # Ensure this is the correct endpoint in Mistral API docs

        headers = {
            "Authorization": f"Bearer {mistral_api_key}",  # Use the key directly here
            "Content-Type": "application/json"
        }
        
        # Prepare the data payload
        data = {
            "input": prompt,  # Adjust based on the actual API parameter names
            "max_tokens": 150  # You can adjust the max tokens as needed
        }

        # Make the API request
        response = requests.post(api_url, headers=headers, json=data)

        # Check if the response is successful
        if response.status_code == 200:
            # Assuming the API responds with a 'choices' field; adjust based on actual API response
            return response.json()['choices'][0]['text']
        else:
            st.error(f"Error: {response.status_code}, Message: {response.text}")  # More detailed error logging
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit UI
st.title("💬 Chatbot - Mental Health Support")
st.write("This is a chatbot powered by Mistral API for mental health support.")

# Take user input for the chatbot prompt
if prompt := st.text_input("Enter your message"):
    # Call Mistral API and get the response
    response = get_mistral_response(prompt)
    
    # Display the response if it's available
    if response:
        st.write(response)


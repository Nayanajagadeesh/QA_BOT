from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("KRUSHI Talk")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input and button for submitting questions
input_text = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input_text:
    response = get_gemini_response(input_text)
    # Add user query to session state chat history
    st.session_state['chat_history'].append(("You", input_text))

    st.subheader("The Response is")

    # Handle the streaming response
    response_text = ""
    for chunk in response:
        if hasattr(chunk, 'candidates') and chunk.candidates:
            for candidate in chunk.candidates:
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        response_text += part.text

    # Display the response text
    if response_text:
        st.write(response_text)
        st.session_state['chat_history'].append(("Bot", response_text))
    else:
        st.write("No valid response received.")

# Display chat history
st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

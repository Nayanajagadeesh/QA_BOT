from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

## Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")

st.header("KRUSHI Talk")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input_text:
    response = get_gemini_response(input_text)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The Response is")

    # Print response for debugging
    st.write("Response object: ", response)

    for chunk in response:
        if hasattr(chunk, 'text'):
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
        else:
            st.write("Chunk does not have a text attribute: ", chunk)

st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

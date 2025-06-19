from dotenv import load_dotenv
import streamlit as st
import os
import re
import google.generativeai as genai
import tiktoken

# Load environment variables
#load_dotenv()
# Explicitly load from `apii.env`
load_dotenv(dotenv_path="apii.env")

# Configure the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Use tokenizer for token counting
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(tokenizer.encode(text))

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    return response_text

st.set_page_config(page_title="Buddy AI")

# Initialize session state
if 'users' not in st.session_state:
    st.session_state['users'] = {}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'token_count' not in st.session_state:
    st.session_state['token_count'] = 0

def validate_password(password):
    if len(password) < 6 or len(password) > 20:
        return False, "Password must be 6-20 characters long."
    if not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one digit."
    if not re.search("[@#$%^&*!]", password):
        return False, "Password must contain at least one special character."
    return True, ""

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def signup(username, password):
    if not validate_email(username):
        st.warning("Invalid email address.")
        return
    valid_password, error_message = validate_password(password)
    if not valid_password:
        st.warning(error_message)
        return
    if username in st.session_state['users']:
        st.warning("User already exists!")
    else:
        st.session_state['users'][username] = password
        st.success("Signup successful! Please log in.")

def login(username, password):
    if username in st.session_state['users'] and st.session_state['users'][username] == password:
        st.session_state['logged_in'] = True
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")

# UI
if not st.session_state['logged_in']:
    st.title("Buddy AI - Login/Signup")
    choice = st.radio("Choose an option", ["Login", "Signup"])
    username = st.text_input("Email (Username)")
    password = st.text_input("Password", type="password")
    if choice == "Signup":
        if st.button("Signup"):
            signup(username, password)
    elif choice == "Login":
        if st.button("Login"):
            login(username, password)
else:
    st.title("Buddy AI")
    input_text = st.text_input("Input:", key="input")
    submit = st.button("Search")

    if submit and input_text:
        input_tokens = count_tokens(input_text)
        response = get_gemini_response(input_text)
        response_tokens = count_tokens(response)
        total_tokens_used = input_tokens + response_tokens
        st.session_state['token_count'] += total_tokens_used

        st.session_state['chat_history'].append(("You", input_text))
        st.session_state['chat_history'].append(("Bot", response))

        st.subheader("Response")
        st.write(response)
        st.write(f"Tokens used in this interaction: {total_tokens_used}")
        st.write(f"Total tokens used: {st.session_state['token_count']}")

    st.subheader("The chat history")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

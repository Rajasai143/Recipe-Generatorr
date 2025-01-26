import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# Configure the Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to create a Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    return response_text

def parse_response(response_text):
    
    # Assuming the response is structured with the recipe name on the first line
    # and the recipe content follows
    lines = response_text.split("\n")
    recipe_name = lines[0].strip() if lines else "Unnamed Recipe"
    recipe_content = "\n".join(lines[1:]).strip() if len(lines) > 1 else "No content available"
    return recipe_name, recipe_content

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="Recipe Generator AI", layout="wide")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")

st.header("Recipe Generator AI")

# Initialize the session state for the chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Text area for user input
input_text = st.text_area("Enter the ingredients you have:", key="input_text")

# Button to submit the ingredients
submit_button = st.button("Generate Recipe")

if submit_button and input_text:
    prompt = f"Generate a recipe using the following ingredients: {input_text}"
    response_text = get_gemini_response(prompt)
    recipe_name, recipe_content = parse_response(response_text)
    
    # Add user query and response to session chat history
    st.session_state["chat_history"].append(("You", input_text))
    
    st.subheader("Generated Recipe:")
    st.markdown(f'<div class="response"><h2>{recipe_name}</h2><p>{recipe_content}</p></div>', unsafe_allow_html=True)
    st.session_state["chat_history"].append(("Bot", f"{recipe_name}\n{recipe_content}"))

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state["chat_history"]:
    if role == "Bot":
        st.markdown(f"**{role}:** {text}")
    else:
        st.write(f"{role}: {text}")

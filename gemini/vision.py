import os
from dotenv import load_dotenv, find_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image

from IPython.display import display
from IPython.display import Markdown

# load all environment variables from .env
load_dotenv(find_dotenv())
# and configure for Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# create your LLM (Google Gemini-Pro)
model = genai.GenerativeModel("gemini-pro-vision")


def get_gemini_response(image, text=None):
    """
    function to call the Google Gemini Pro model & get response
    for image & optional text
    """
    params = [text, image] if text is not None else image
    response = model.generate_content(params)
    return response.text


st.set_page_config(page_title="Q&A Demo", page_icon="♊️")
st.header("Q&A with Gemini Pro Image 🖼️")
# create an input text and upload for image
question = st.text_input("Input: ", key="question")
uploaded_file = st.file_uploader("Choose image...", type=["jpg", "jpeg", "png", "tiff"])
image = ""
submit = st.button("Ask Away")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

if submit:
    response = get_gemini_response(image, question)
    st.write(response)

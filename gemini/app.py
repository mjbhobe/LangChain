import os
from dotenv import load_dotenv, find_dotenv
import streamlit as st
import google.generativeai as genai
import textwrap

from IPython.display import display
from IPython.display import Markdown

# load all environment variables from .env
load_dotenv(find_dotenv())
# and configure for Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# create your LLM (Google Gemini-Pro)
model = genai.GenerativeModel("gemini-pro")


def get_gemini_response(question):
    """function to call the Google Gemini Pro model & get response"""
    response = model.generate_content(question)
    return response.text


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


st.set_page_config(page_title="Q&A Demo", page_icon="♊️")
st.header("♊️ Q&A with Gemini Pro ️🪄")
# create an input text and submit button
question = st.text_input("Input: ", key="question")
submit = st.button("Ask Away")

if submit:
    # submit button is clicked
    response = get_gemini_response(question)
    st.write(response)

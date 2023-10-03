# test.py - test if I can call OpenAPI
import os
import openai
from langchain.llms import OpenAI
import streamlit as st


# setup the OpenAI API Key (read from file)
OPEN_API_KEY_FILE = r"c:\dev\OpenAIKey.txt"
if not os.path.exists(OPEN_API_KEY_FILE):
    raise FileNotFoundError(f"OpenAI API key file not found at {OPEN_API_KEY_FILE}")

OPEN_API_KEY = None
with open(OPEN_API_KEY_FILE, "r") as f:
    OPEN_API_KEY = f.read().strip()
os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

# initialize Streamlit page
st.title("LangChain demo with OpenAI API")
input_text = st.text_input("Search the topic you want")

llm = OpenAI(temperature=0.8)

if input_text:
    # just display response from LLM
    st.write(llm(prompt=input_text))



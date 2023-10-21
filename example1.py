# example1.py - using prompts with OpenAI API
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st


# # setup the OpenAI API Key (read from file)
# OPEN_API_KEY_FILE = r"c:\dev\OpenAIKey.txt"
# if not os.path.exists(OPEN_API_KEY_FILE):
#     raise FileNotFoundError(f"OpenAI API key file not found at {OPEN_API_KEY_FILE}")

# OPEN_API_KEY = None
# with open(OPEN_API_KEY_FILE, "r") as f:
#     OPEN_API_KEY = f.read().strip()
# os.environ["OPENAI_API_KEY"] = OPEN_API_KEY
load_dotenv()

# initialize Streamlit page
st.title("Celebrity Search Results")
input_text = st.text_input("Enter name of celebrity to get an interesting titbit")

# the LLM to use
llm = OpenAI(temperature=0.7)

# prompt template
input_prompt1 = PromptTemplate(
    input_variables=["name"],
    template="Tell me about {name}",
)

chain1 = LLMChain(llm=llm, prompt=input_prompt1, verbose=True)

if input_text:
    # just display response from LLM
    st.write(chain1.run(input_text))

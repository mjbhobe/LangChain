# restaurants-1.py - paramaterise a prompt
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st


# setup the OpenAI API Key (read from file)
OPEN_API_KEY_FILE = r"c:\dev\OpenAIKey.txt"
if not os.path.exists(OPEN_API_KEY_FILE):
    raise FileNotFoundError(f"OpenAI API key file not found at {OPEN_API_KEY_FILE}")

OPEN_API_KEY = None
with open(OPEN_API_KEY_FILE, "r") as f:
    OPEN_API_KEY = f.read().strip()
os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

# Part-1: Ask the LLM (OpenAI in this case) to suggest name of a restaurant
# for a certain type of cuisine (for example Mexican, Italian, Indian etc.)

# instantiate our LLM
llm = OpenAI(temperature=0.7)

# create a prompt template
prompt_template_name = PromptTemplate(
    input_variables=["cuisine"],
    template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for it",
    verbose=True,
)

# create a chain with LLM & template
chain = LLMChain(llm=llm, prompt=prompt_template_name)

# let's ask the chain for a fancy name for different types of cuisines
cuisine = "Korean"
response = chain.run(cuisine).strip()
print(f"{cuisine} -> {response}")

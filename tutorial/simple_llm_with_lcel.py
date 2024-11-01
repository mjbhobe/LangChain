import os
from dotenv import load_dotenv, find_dotenv

import os
from langchain_openai import ChatOpenAI


# load API keys from local .env file
load_dotenv(find_dotenv())

# create instance of OpenAI GPT-4
model = ChatOpenAI(model="gpt-4")

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

english_message = "Hello, Good morning! Welcome to Langchain tutorial with OpenAI"

messages = [
    SystemMessage(content="Translate the following from English to French"),
    HumanMessage(content=english_message),
]
response = model.invoke(messages)
parser = StrOutputParser()
print(f"Translating English to French")
print(f"English: {english_message}")
print(f"Translation: {parser.invoke(response)}")

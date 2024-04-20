""" hello_gemini.py: Hello Google Gemini"""

import pathlib
import textwrap
import os
from dotenv import load_dotenv, find_dotenv

import google.generativeai as genai

# Used to securely store your API key
# from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown

# load env variables from .env file
_ = load_dotenv(find_dotenv())  # read local .env file
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def to_markdown(text):
    """function to convert response from model to correct format"""
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def main():
    # list all available models
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)

    # we'll use the only available model
    llm = genai.GenerativeModel("gemini-pro")
    prompt_text = ""
    while True:
        prompt_text = input("Enter your question: ")
        if prompt_text.lower() == "quit":
            break
        try:
            response = llm.generate_content(prompt_text)
            print("\n")
            print(response.text)
            print("-" * 80)
        except ValueError as err:
            print(f"Error: {err}")
            print(f"{response.prompt_feedback}")


if __name__ == "__main__":
    main()

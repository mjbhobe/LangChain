"""
hello_gemini.py: Hello Google Gemini
This script demonstrates how to use the Google Gemini model as a chatbot

@author: Manish Bhobe
My experiments with Python, ML, Gen AI, and more
Code shared for educational purposes only. Use at your own risk!!
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

import google.generativeai as genai

# load env variables from .env file
_ = load_dotenv(override=True)  # read local .env file
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# for colorful output
console = Console()


def to_markdown(text):
    """function to convert response from model to correct format"""
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def main():
    # list all available Google models
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)

    # we'll be using the gemini-2.5-flash model
    # you can choose any model from the list displayed above
    # if you want to use a different model, change the model name below
    llm = genai.GenerativeModel("gemini-2.5-flash")
    prompt_text = ""
    console.print(
        Markdown(
            "Enter your question below **or** type _quit_ or _bye_ or _exit_ to end the chat",
            style="blue",
        )
    )
    while True:
        console.print("[green]You? [/green]", end="")
        prompt_text = input()
        if prompt_text.lower() in ["bye", "quit", "exit"]:
            break
        try:
            response = llm.generate_content(prompt_text)
            console.print("[yellow]AI: [/yellow]")
            console.print(Markdown(response.text))
        except ValueError as err:
            console.print(f"[red]Error:[/red]\n{err}")
            print(f"{response.prompt_feedback}")


if __name__ == "__main__":
    main()

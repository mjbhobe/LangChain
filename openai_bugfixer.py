#!/usr/bin/env python
"""
* openai_bugfixer.py: leverage OpenAI GPT-3.5-Turbo model to resolve bugs in code
"""
import os
import pathlib
from dotenv import load_dotenv
import openai

system_prompt = "You will be provided with a piece of Python code, and your task is to find and fix bugs in it."

# following is a piece of buggy code
# with syntax as well as logical errors
code_to_debug = """
import Random
a = random.randint(1,12)
b = random.randint(1,12)
for i in range(10):
    question = "What is "+a+" x "+b+"? "
    answer = input(question)
    if answer = a//b
        print (Well done!)
    else:
        print("No.")
"""


def main():
    # load environment variables from .env - this seems to create a problem with Streamlit reload
    load_dotenv()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{code_to_debug}"},
        ],
    )
    print(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()

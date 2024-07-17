import os
from dotenv import load_dotenv, find_dotenv

import streamlit as st
import os
import google.generativeai as genai


# load API keys from local .env file
load_dotenv(find_dotenv())
# configure API access with key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# (Optional) - set the configuration that controls how responses are generated
# by the Gemini model
config = genai.GenerationConfig(
    temperature=0.0,
    # response_mime_type="application/json",
)

# create the Gemini model for use - we'll use flash
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=config,
)


# get response from Gemini model
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text


def main():
    question = """
        When is Deepika Padukone's birthday? Who won the ICC World cup in the year she was born?
    """
    print(get_gemini_response(question))

    # st.set_page_config(page_title="Q&A Demo with Google Gemini")
    # st.header("Ask Gemini Flash anything")
    # input = st.text_input("Your question:", key="input")
    # submit = st.button("Go!")

    # if submit:
    #     if input.strip() != "":
    #         # only if we have a question
    #         response = get_gemini_response(input)
    #         st.write(response)
    #     else:
    #         st.write("Please enter a question I can respond to!")


# if __name__ == "__main__":
#     main()

main()

# restaurants.py - a Stremlit based application to recommend a restaurant name
# and menu items. It's always better to show an end-user a web based interface
# rather than an iPython notebook.

# pre-requisits:
# Install streamlit using: pip install streamlit
# run this file (in the file's folder) using: streamlit run restaurants.py
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import streamlit as st


def main():
    # load environment variables from .env
    load_dotenv()
    print(os.environ["HELLO"])

    # setup the OpenAI API Key (read from file)
    OPEN_API_KEY_FILE = r"c:\dev\OpenAIKey.txt"
    if not os.path.exists(OPEN_API_KEY_FILE):
        raise FileNotFoundError(f"OpenAI API key file not found at {OPEN_API_KEY_FILE}")

    OPEN_API_KEY = None
    with open(OPEN_API_KEY_FILE, "r") as f:
        OPEN_API_KEY = f.read().strip()
    os.environ["OPENAI_API_KEY"] = OPEN_API_KEY

    # setup our interface with Streamlit
    st.title("Restaurant name &amp; menu generator")

    # create a side-bar to select a cuisine from the following
    cuisines = (
        "American",
        "Mexican",
        "Indian",
        "Chinese",
        "Italian",
        "Thai",
        "Vietnamese",
        "Japanese",
        "Lebanese",
        "French",
    )
    # capture user's selection to a variable
    cuisine = st.sidebar.selectbox("Pick a cuisine", sorted(cuisines))

    # following runs only if user selects any item
    if cuisine:
        st.markdown(
            f"Will generate a name for a **{cuisine}** restaurant with sample menu items"
        )


if __name__ == "__main__":
    main()

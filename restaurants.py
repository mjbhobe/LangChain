# restaurants.py - a Stremlit based application to recommend a restaurant name
# and menu items. It's always better to show an end-user a web based interface
# rather than an iPython notebook.

# pre-requisits:
# Install streamlit using: pip install streamlit
# run this file (in the file's folder) using: streamlit run restaurants.py
import os
import pathlib
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import streamlit as st


def get_restaurant_name_and_items(cuisine: str):
    # our llm
    llm = OpenAI(temperature=0.6)

    # prompt template for the restaurant name, given a cuisine
    prompt_template_name = PromptTemplate(
        # you can have multiple input variables, hence the list
        input_variables=["cuisine"],
        # this is your prompt - same as above except the cuisine is parameterised with {}
        # similar to a Python f-string
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for it. Only one name please.",
    )

    name_chain = LLMChain(
        llm=llm,
        prompt=prompt_template_name,
        # here we add an output_key parameter to capture the output from this prompt
        output_key="restaurant_name",
    )

    # prompt template for menu items given a restaurant name
    prompt_template_menu = PromptTemplate(
        # you can have multiple input variables, hence the list
        input_variables=["restaurant_name"],
        # this is your prompt - same as above except the cuisine is parameterised with {}
        # similar to a Python f-string
        template="Please suggest 10-15 menu items for {restaurant_name}. Return as comma separated list",
    )

    # chain is the same as before
    menu_chain = LLMChain(
        llm=llm,
        prompt=prompt_template_menu,
        # here we add an output_key parameter to capture the output from this prompt
        output_key="menu_items",
    )

    from langchain.chains import SequentialChain

    seq_chain = SequentialChain(
        chains=[name_chain, menu_chain],  # NOTE: sequence matters here!!
        input_variables=["cuisine"],  # input variable to first chain in sequence
        # NOTE: here we specify the output variables too
        output_variables=["restaurant_name", "menu_items"],
    )

    # now we execute the chain. Note how the call is a bit different
    response = seq_chain({"cuisine": cuisine})
    return response


def main():
    # load environment variables from .env - this seems to create a problem with Streamlit reload
    # load_dotenv()
    # print(os.environ["OPENAI_API_KEY"])

    # setup the OpenAI API Key (read from file)
    # OPEN_API_KEY_FILE =  r"c:\dev\OpenAIKey.txt"
    OPEN_API_KEY_FILE = pathlib.Path(__file__).parent / ".env"
    if not os.path.exists(OPEN_API_KEY_FILE):
        raise FileNotFoundError(f"OpenAI API key file not found at {OPEN_API_KEY_FILE}")

    OPENAI_API_KEY = None
    with open(OPEN_API_KEY_FILE, "r") as f:
        # OPEN_API_KEY = f.read().strip()
        OPENAI_API_KEY = f.read().strip().split("=")[1].strip()  # grab second token
        # print(f"OPENAI_API_KEY = {OPENAI_API_KEY}")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

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
    # cuisine = "Arabic"

    # following runs only if user selects any item
    if cuisine:
        response = get_restaurant_name_and_items(cuisine)
        # print(response)
        # display the results
        st.header(f"Welcome to _{response['restaurant_name'].strip()}_")
        st.text("We are happy to serve you. Please pick your items from menu:")
        for item in response["menu_items"].strip().split(","):
            st.markdown(f"* {item}")


if __name__ == "__main__":
    main()
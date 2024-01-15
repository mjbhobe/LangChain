"""
llama2_app1.py - create blogs using locally downloaded LLama2 model
"""
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers


# function to get response from local LLama2 model
def getLlamaResponse(blog_topic, num_words, target_audience):
    """call the local Llama2 model, downloaded into the models directory"""
    local_llm_path = "models/llama-2-7b-chat.ggmlv3.q8_0.bin"
    llm = CTransformers(
        model=local_llm_path,
        model_type="llama",
        config={"max_new_tokens": 256, "temperature": 0},
    )

    # define the prompt template
    template = """
    Write a blog for {target_audience} job profile for the topic {blog_topic}
    no more than {num_words} words.
    """
    prompt = PromptTemplate(
        input_variables=["blog_topic", "num_words", "target_audience"],
        template=template,
    )

    # generate response from local llm
    response = llm(
        prompt.format(
            blog_topic=blog_topic, num_words=num_words, target_audience=target_audience
        )
    )
    return response


# code entry point
st.set_page_config(
    page_title="Llama Blogs Generator",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.header("Llama - 🦙🦙: Blog Generator")
blog_topic = st.text_input("Enter a topic for the blog")
col1, col2 = st.columns([5, 5])
with col1:
    num_words = st.text_input("No of words")
with col2:
    target_audience = st.selectbox(
        "Target audience of blog",
        ["Researchers", "Data Scientists", "Common People"],
        index=0,
    )
submit = st.button("Generate")

if submit:
    st.write(getLlamaResponse(blog_topic, num_words, target_audience))
    # st.write(
    #     f"Will generate a blog about '{blog_topic}' of '{num_words}' words for '{target_audience}'"
    # )

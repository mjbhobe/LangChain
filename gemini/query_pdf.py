#!/usr/bin/env python
"""
query_pdf.py - illustrates how to interface Gemini Pro LLM with PDFs as 
a knowledge retriever
"""
import os
import textwrap
from dotenv import load_dotenv, find_dotenv
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from IPython.display import display
from IPython.display import Markdown

# load all environment variables from .env
load_dotenv(find_dotenv())
# and configure API key for Google Geimini access
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# create your LLM (Google Gemini-Pro)
# model = genai.GenerativeModel("gemini-pro")


def get_pdf_text(pdfs):
    """read all text from all PDFs provided"""
    text = ""
    for pdf in pdfs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10_000, chunk_overlap=1_000
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    # save locally (you can also save it to database or other location)
    vector_store.save_local("faiss_index")


def get_conversational_chain(temperature=0.3):
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, 
    if the answer is not in provided context just say, "answer is not available in the context", don't provide 
    the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    # initialize chat model with Gemini-pro backend
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=temperature)
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt, verbose=True)
    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    context_db = FAISS.load_local("faiss_index", embeddings)
    docs = context_db.similarity_search(user_question)
    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True,
    )
    print(response)
    st.write("Reply:", response["output_text"])


def get_gemini_response(question):
    """function to call the Google Gemini Pro model & get response"""
    response = model.generate_content(question)
    return response.text


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon="♊️")
    st.header("Q&A with PDFs using Gemini Pro ♊️")

    user_question = st.text_input("Ask a question from PDF files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDFs and click the Submit button",
            accept_multiple_files=True,
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()

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
from PyPDF3 import PdfReader
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
model = genai.GenerativeModel("gemini-pro")


def get_pdf_text(pdfs):
    """read all text from all PDFs provided"""
    text = ""
    for pdf in pdfs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_gemini_response(question):
    """function to call the Google Gemini Pro model & get response"""
    response = model.generate_content(question)
    return response.text


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))

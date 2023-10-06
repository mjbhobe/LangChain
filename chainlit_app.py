# -*- coding: utf-8 -*-
"""
chainlit_app.py: basic chainlit application with TII Falcon 7 Bn model on Hugging Face
to run: $> chainlit run chainlit_app.py -w
"""

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub
import chainlit as cl

template = """
You are an AI assistant who gives helpful, detailed and polite answers to the user's questions.

{question}
"""


@cl.on_chat_start
def main():
    """initializations when the chat starts"""
    # load all API keys from .env file
    load_dotenv()

    # we'll be using the Falcon 7 Bn model on HuggingFace Hub
    repo_id = "tiiuae/falcon-7b-instruct"
    llm = HuggingFaceHub(
        repo_id=repo_id,
        huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
        model_kwargs={"temperature": 0.6, "max_new_tokens": 2000},
    )
    prompt_template = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt_template, llm=llm, verbose=True)
    # store chain in user's session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    """will be called every time a user submits a prompt on chat window"""
    # add your custom logic here..
    llm_chain = cl.user_session.get("llm_chain")
    # call chain asynchronously
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # post processing

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["text"]).send()

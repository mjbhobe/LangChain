import os
from dotenv import load_dotenv, find_dotenv

# load API keys from local .env file
load_dotenv(find_dotenv())


# create LLM based on value of LLM_TO_USE
if os.environ["LLM_TO_USE"] == "openai":
    from langchain_openai import ChatOpenAI

    model = ChatOpenAI(model="gpt-4")
    print("Using OpenAI model")
elif os.environ["LLM_TO_USE"] == "gemini":
    from langchain_google_genai import ChatGoogleGenerativeAI

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )
    print("Using ChatGoogleGenerativeAI -> gemini-1.5-pro model")

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

SYSTEM_MESSAGE = "Translate the following from English into French"
USER_MESSAGE = "I love the Langchain framework!"

messages = [
    SystemMessage(content=SYSTEM_MESSAGE),
    HumanMessage(content=USER_MESSAGE),
]

print(SYSTEM_MESSAGE)
print(USER_MESSAGE)

result = model.invoke(messages)
parser = StrOutputParser()
print(f">> {parser.invoke(result)}")

print("Using LCEL instead")
chain = model | parser

print(SYSTEM_MESSAGE)
print(USER_MESSAGE)
print(f">> {chain.invoke(messages)}")

# using prompt template
from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following from English into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
result = prompt_template.invoke({"language": "French", "text": USER_MESSAGE})
print(f">> {result.to_messages()}")

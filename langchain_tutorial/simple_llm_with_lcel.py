import os
from dotenv import load_dotenv
from rich import print

# load API keys from local .env file
load_dotenv(override=True)


def get_model():
    # create LLM based on value of LLM_TO_USE in .env file
    if os.environ["LLM_TO_USE"] == "openai":
        from langchain_openai import ChatOpenAI

        model = ChatOpenAI(model="gpt-4")
        print("Using OpenAI model")
    elif os.environ["LLM_TO_USE"] == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
        print("Using ChatGoogleGenerativeAI -> gemini-2.5-flash model")
    return model


model = get_model()
response = model.invoke("Hello World!")
print("Response:")
print(response)

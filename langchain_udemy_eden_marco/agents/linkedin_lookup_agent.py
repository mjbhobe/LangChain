import os
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub


def lookup(name: str) -> str:
    """lookup the LinkedIn profile URL for a given name

    Args:
        name (str): name of person whose LinkedIn profile URL is to be found

    Returns:
        profile URL (str)
        e.g. for user Manish Bhobé, it should return
        URL https://www.linkedin.com/in/manish-bhobe-b57a6a2/
    """
    # begin with hard coded URL
    # return "https://www.linkedin.com/in/eden-marco"

    # create our LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

    # define our prompt template
    prompt: str = """
    Given the name {name_of_person} I want you to get me the URL of their
    LinkedIn profile page. Your answer should contain ONLY the URL.
    """
    prompt_template = PromptTemplate(
        template=prompt,
        input_variables=["name_of_person"],
    )

    # define the tool for our LLM
    search_tool = Tool(
        name="Crawl Google for LinkedIn profile page",
        # description is SUPER important as LLM uses this to decide which tool
        # to use according to its reasoning agent
        description="Useful for when you have to retrieve the LinkedIn profile URL",
        function="?",
    )


# testing stub
if __name__ == "__main__":
    name: str = "Eden Marco"
    profile_url = lookup(name)
    print(f"Profile URL for {name} -> {profile_url}")

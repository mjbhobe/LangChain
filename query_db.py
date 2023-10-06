"""
query_db.py - illustrates how you can use LangChain to enable an LLM
to query a database
"""
import os
import dotenv
import pathlib
import urllib.parse

# import psycopg2
from configparser import ConfigParser
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType


def get_dbconnect_uri() -> str:
    parser = ConfigParser()
    # configuration file (INI format) holding connection params
    config_file_path = pathlib.Path(__file__).parent / "config.ini"
    # section holding the connection info (you can have other sections too)
    section = "postgres"

    assert os.path.exists(
        config_file_path
    ), f"FATAL: Configuration file {config_file_path} does not exist!"
    parser.read(config_file_path)

    # read params from section
    connect_params = {}
    connection_uri = ""
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            connect_params[param[0]] = param[1]
        # URL encode connection params, useful if you are using special characters
        # in user id, server name, db name or password
        server = urllib.parse.quote(connect_params["server"])
        user = urllib.parse.quote(connect_params["user"])
        password = urllib.parse.quote(connect_params["password"])
        database = urllib.parse.quote(connect_params["database"])
        # PostgreSQL URI ->postgresql://username:password@dbserver:port/database
        connection_uri = f"postgresql://{user}:{password}@{server}:{connect_params['port']}/{database}"
    else:
        raise ValueError(f"FATAL: {config_file_path} does not have section {section}!")

    return connection_uri


def chat_with_database(agent):
    print(
        "Chat with your database. Enter your prompt or type 'exit' (without quotes) to quit"
    )

    while True:
        prompt = input("Prompt? ")
        if prompt.lower() == "exit":
            print("Thank you and Goodbye!")
            break
        else:
            try:
                print(agent.run(prompt))
            except Exception as e:
                print(e)


def main():
    dotenv.load_dotenv()
    # db_connect_params = get_dbconnect_params()
    # conn = psycopg2.connect(**db_connect_params)
    db_conn_uri = get_dbconnect_uri()
    # connect to database
    db = SQLDatabase.from_uri(db_conn_uri)
    # instantiate my llm
    llm = OpenAI(temperature=0, verbose=True)
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    chat_with_database(agent_executor)


if __name__ == "__main__":
    main()

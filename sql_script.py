from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from sqlalchemy import create_engine
import mysql.connector
from langchain_community.llms import Ollama


cs="mysql+mysqlconnector://tushar:hcdc@localhost/MMRHIS"
db_engine=create_engine(cs)
db=SQLDatabase.from_uri(cs)



llm = Ollama(model='mistral')  
sql_toolkit=SQLDatabaseToolkit(db=db,llm=llm)
sql_toolkit.get_tools()



agent=create_sql_agent(llm=llm,toolkit=sql_toolkit,verbose=False)
print(agent.invoke("how many tables are there in MMRHIS database"))
# import streamlit as st
# from langchain_community.agent_toolkits.sql.base import create_sql_agent
# from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
# from langchain.agents.agent_types import AgentType
# from langchain.chat_models import ChatOpenAI  # Consider using OpenAI API for ChatGPT-like experience
# from langchain_community.utilities import SQLDatabase
# from langchain.prompts.chat import ChatPromptTemplate
# from sqlalchemy import create_engine
# import mysql.connector
# from langchain_community.llms import Ollama


# def create_sql_connection(user, password, database, host="localhost"):
#     """Creates a secure SQL connection using environment variables or user input."""

#     try:
#         # Prioritize environment variables for security
#         db_user = st.secrets.get("DB_USER") or st.text_input("Username")
#         db_password = st.secrets.get("DB_PASSWORD") or st.text_input("Password", type="password")
#         db_host = st.secrets.get("DB_HOST") or host
#         db_name = st.text_input("Database Name")

#         if not all([db_user, db_password, db_name]):
#             st.error("Please provide all database credentials.")
#             return None

#         connection_string = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
#         engine = create_engine(connection_string)
#         return SQLDatabase.from_uri(connection_string)

#     except Exception as e:
#         st.error(f"Error connecting to database: {e}")
#         return None


# def main():
#     """
#     Streamlit app entry point.
#     Handles user interaction and creates/runs the SQL agent.
#     """

#     st.title("SQL Agent with Streamlit Chat Interface")

#     db = create_sql_connection(user=None, password=None, database=None)

#     if not db:
#         st.stop()
#         return

#     llm = Ollama(model="mistral")
#     sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
#     sql_toolkit.get_tools()
#     agent = create_sql_agent(llm=llm, toolkit=sql_toolkit, verbose=False)

#     # Chat interface
#     chat_history = []
#     user_message = st.text_input("Ask your question about the database:")

#     if user_message:
#         chat_history.append({"message": user_message, "agent": False})
#         agent_response = agent.run(user_message)
#         chat_history.append({"message": agent_response, "agent": True})

#         for message in chat_history:
#             st.write(message["message"] if message["agent"] else f"**You:** {message['message']}")

# if __name__ == "__main__":
#     main()

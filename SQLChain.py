from langchain_community.utilities import SQLDatabase
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI  # Consider using OpenAI API for ChatGPT-like experience
from langchain_community.utilities import SQLDatabase
from langchain.prompts.chat import ChatPromptTemplate
from sqlalchemy import create_engine
import mysql.connector
from langchain_community.llms import Ollama
import emoji


#Initializing databse Connection
def init_database(user: str, password: str, host: str, port: str, database: str):
  db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
  return SQLDatabase.from_uri(db_uri)


# Define llm outside the function for reuse
llm = Ollama(model='mistral')  

def get_response(user_query: str, db: SQLDatabase, chat_history: list):
  sql_toolkit=SQLDatabaseToolkit(db=db,llm=llm)
  agent=create_sql_agent(llm=llm,toolkit=sql_toolkit,verbose=False,handle_parsing_errors=True)
  
  return agent.run(input=user_query)    
  
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]


st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:")

st.title("Chat with MySQL")

with st.sidebar:
    st.subheader("Mysql user setting")

    
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value="tushar", key="User")
    st.text_input("Password", type="password", value="hcdc", key="Password")
    st.text_input("Database", value="MMRHIS", key="Database")
    
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            st.session_state.db = db
            st.success("Connected to database!")
    
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    with st.chat_message("AI"):
        try:
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.markdown(response)
        except:
            response = emoji.emojize("Please review your prompt and ensure it focuses solely on database-related questions with adequate detail. :thumbs_up:")
            st.markdown(response)
        
    st.session_state.chat_history.append(AIMessage(content=response))

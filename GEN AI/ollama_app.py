##UI -- webpage ---> streamlit 
##simple aur basic types of projects 
# easy lib because in this you  have to use html and css 

import os 
from dotenv import load_dotenv

from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

##langchain tracking 
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


#prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant.Please respond to the question asked"),
        ("human", "{question}"),
    ]
)

##streamlit 
st.title("Ollama App")
input_text = st.text_input("Enter your question:")


##ollama 
llm = Ollama(model = "gemma:2b")
outparser = StrOutputParser()
chain = prompt | llm | outparser

if input_text:
   st.write(chain.invoke({"question": input_text}))
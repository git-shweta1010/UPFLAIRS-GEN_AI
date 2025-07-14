import streamlit as st 
import openai 
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import os 
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A chatbot 2 june"

##prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant.Please respond to the question asked"),
        ("human", "{question}"),
    ]
)

def generate_response(question, llm , temperature , max_tokens):
    llm = Ollama(model = llm)
    output_perser = StrOutputParser()
    chain = prompt | llm | output_perser
    answer = chain.invoke({"question" : question})
    return answer

##title 
st.title("Simple Q&A chatbot")

##select the openai model 
llm  = st.sidebar.selectbox(
    "Select Open Source Model",
    ["mistral"]
)

##temperature 
temperature = st.sidebar.slider("Temperature", 
                                min_value=0.0, 
                                max_value=1.0,
                                  value=0.7)

##max tokens 
max_tokens = st.sidebar.slider("Max Tokens", 
                                min_value=50, 
                                max_value=300,
                                  value=150)
#main interface 
st.write("Enter your question")
user_input = st.text_area("You:")

if user_input:
    response = generate_response(user_input, llm, temperature, max_tokens)
    st.write("Bot:")
    st.write(response)
else:
    st.write("Please enter a question.")
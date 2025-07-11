import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain,LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import initialize_agent, Tool
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from dotenv import load_dotenv
load_dotenv()

##set ui for st app 
st.set_page_config(
    page_title="MathsGPT",
    page_icon="😎",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("MathsGPT")

groq_api_key = st.sidebar.text_input(label="Groq API Key"
                                     , type="password")

if not groq_api_key:
    st.info("Please add your Groq API key to continue.")
    st.stop()

llm = ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

##initial tools 
wiki_wrapper = WikipediaAPIWrapper()
##search and retrieve summary/data from the wikipidia
wiki_tool = Tool(
    name="Wikipedia",
    func=wiki_wrapper.run,
    description="useful for when you need to answer questions about current events",
)

##math tool 
math_chain = LLMMathChain.from_llm(llm=llm)
##a LLMmath chain -- special chain to allow LLM to solve maths problem 
#using reasoning and calculator like backend 
calculator = Tool(
    name = "Calculator",
    func = math_chain.run,
    description = "useful for when you need to answer questions about math",
    
)

##prompt 
prompt="""
Your a agent tasked for solving users mathemtical question. 
Logically arrive at the solution and provide a detailed explanation
and display it point wise for the question below
Question:{question}
Answer:
"""

prompt_template = PromptTemplate(
    template=prompt, input_variables=["question"]
)

##combine all the tools into chain 
chain = LLMChain(llm=llm,prompt=prompt_template)

resoning_tool = Tool(
    name="Reasoning",
    func=chain.run,
    description="useful for when you need to answer questions about current events",
)

##agent
assistant_agent = initialize_agent(
    tools  = [wiki_tool,calculator,resoning_tool],
    llm = llm,
    agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose = False,
    handle_parsing_errors = True    
) 

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How can I help you today?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

##lets start the conversation
question = st.text_area(" ")

if st.button("Find my answer"):
    if question:
        with st.spinner("Thinking..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response = assistant_agent.run(st.session_state.messages, 
                                           callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", 
                                              "content": response})
            st.write("Response:")
            st.success(response)

    else:
        st.warning("Please enter a question.")            

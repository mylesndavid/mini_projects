from dotenv import load_dotenv
import os
import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

load_dotenv()

key = os.environ['API_KEY']

# App framework 
st.title('GPTWIN')
prompt = st.text_input('Plug in prompt here')

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'write me a youtube title about {topic}'
)
script_template = PromptTemplate(
    input_variables = ['title','wikipedia_research'],
    template = 'write me a youtube video script about this title TITLE: {title}  but also while leveraging this wikipedia research {wikipedia_research}'
)

#Memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

#LLMS 
llm = OpenAI(temperature=0.9,openai_api_key=key)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title',memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True,output_key='script',memory=script_memory)
#sequential_chain = SequentialChain(chains=[title_chain,script_chain], input_variables= ['topic'], output_variables=['title','script'], verbose=True)

wiki = WikipediaAPIWrapper()

#show to screen if there is a prompt
if prompt:
    #response = sequential_chain({'topic': prompt})
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    script = script_chain.run(title = title, wikipedia_research = wiki_research)

    # st.write(response['title'])
    # st.write(response['script'])
    st.write(title)
    st.write(script)

    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Script History'):
        st.info(script_memory.buffer)
    
    with st.expander('Wikipedia Research'):
        st.info(wiki_research)
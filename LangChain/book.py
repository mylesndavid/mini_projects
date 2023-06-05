from dotenv import load_dotenv
import os
import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

load_dotenv()

key = os.environ['API_KEY']

# App framework 
st.title('GPTWIN')
prompt = st.text_input('Plug in prompt here')

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'write me a book title about {topic}'
)
first_template = PromptTemplate(
    input_variables = ['title'],
    template = 'write me a first short story chapter about this title number this chapter "Chapter One" and give it a releveant title TITLE: {title}'
)
next_template = PromptTemplate(
    input_variables = ['first'],
    template = ' Give the chapter a title and number write me the next chapter for a short story that comes after this chapter: {first}'
)

#LLMS 
llm = OpenAI(temperature=0.9,openai_api_key=key)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title')
first_chain = LLMChain(llm=llm, prompt=first_template, verbose=True,output_key='first')
next_chain = LLMChain(llm=llm, prompt=next_template, verbose=True,output_key='next')
third_chain = LLMChain(llm=llm, prompt=next_template, verbose=True,output_key='third')
sequential_chain = SequentialChain(chains=[title_chain,first_chain,next_chain,third_chain], input_variables= ['topic'], output_variables=['title','first','next','third'], verbose=True)


#show to screen if there is a prompt
if prompt:
    response = sequential_chain({'topic': prompt})
    st.write(response['title'])
    st.write(response['first'])
    st.write(response['next'])
    st.write(response['third'])
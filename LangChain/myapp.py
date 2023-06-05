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
    template = 'write me a blog title about {topic}'
)
post_template = PromptTemplate(
    input_variables = ['title'],
    template = 'write me a blog post this title TITLE: {title}'
)
analysis_template = PromptTemplate(
    input_variables = ['post'],
    template = 'act as an a critic and analyze this blog post POST: {post}'
)
revised_template = PromptTemplate(
    input_variables = ['analysis'],
    template = 'write me a second blog post that addresses the issues about the blog post mentioned in the analysis ANALYSIS: {analysis}'
)

#LLMS 
llm = OpenAI(temperature=0.9,openai_api_key=key)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title')
post_chain = LLMChain(llm=llm, prompt=post_template, verbose=True,output_key='post')
analysis_chain = LLMChain(llm=llm, prompt=analysis_template, verbose=True,output_key='analysis')
revised_chain = LLMChain(llm=llm, prompt=revised_template, verbose=True,output_key='revision')
sequential_chain = SequentialChain(chains=[title_chain,post_chain,analysis_chain,revised_chain], input_variables= ['topic'], output_variables=['title','post','analysis','revision'], verbose=True)


#show to screen if there is a prompt
if prompt:
    response = sequential_chain({'topic': prompt})
    st.write(response['title'])
    st.write(response['post'])
    st.write(response['analysis'])
    st.write(response['revision'])
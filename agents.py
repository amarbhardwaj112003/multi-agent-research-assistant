from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_web_page
import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq 

load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv('OPENAI_API_KEY'))
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=1)
# First Agent 

def build_search_agent():
    return create_agent(model=llm, tools=[web_search])

# Second Agent
def build_reader_agent():
    return create_agent(model=llm, tools=[scrape_web_page])

# Writer Chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer that writes a comprehensive research report based on the information provided by the search and reader agents. The report should be well-structured, clear, and concise."),
    ("human", """" Write a detailed research report on the topic below. 
     
     Topic: {topic}
     Research Gathered): {research} 

     Structure the report as : 
     - Introduction
     - Key Findings 
     - Conclusion
     - sources (list all urls found in the research)

     Be detailed, factual and professional.
     """)
]) 

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain 

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive resarch critic. Be honest and specific."),
    ("human", """ Review the research report below and evaluate it strictly. 

     Report: {report}

     Respond in this exact format:
     Score : X/10 

     Strengths: List the strengths of the report.
     
     Area to Improve: List the weaknesses and areas of improvement for the report. Be specific and constructive.
     
     one line vedict : ... """), ])

critic_chain = critic_prompt | llm | StrOutputParser()




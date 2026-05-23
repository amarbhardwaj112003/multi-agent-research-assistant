from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

@tool 
def web_search(query: str) -> str:
    """ Search the web for recent and reliable information on a topic. Return Titles, URL 
  and snippets of the search results. """
    search_results = tavily.search(query=query, num_results=2,max_results=2)
    formatted_results = []
    print(search_results)
    for result in search_results['results']:
        title = result['title']
        url = result['url']
        snippet = result['content']
        formatted_results.append(f"Title: {title}\nURL: {url}\ncontent: {snippet}\n")
    return "\n".join(formatted_results)

@tool
def scrape_web_page(url: str) -> str:
    """ Scrape the content of a web page given its URL. Return the main text content of the page. """
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = "\n".join([para.get_text() for para in paragraphs])
        return content
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return "Error occurred while scraping the web page."

# Unittest 
result = web_search.invoke("What is the latest research on multi-agent systems?")
print(result)

scrapper_result = scrape_web_page.invoke("https://en.wikipedia.org/wiki/Multi-agent_system")
print(scrapper_result)



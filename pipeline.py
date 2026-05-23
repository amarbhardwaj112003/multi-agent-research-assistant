from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
from tools import web_search, scrape_web_page
from rich import print

def run_research_pipeline(topic : str) -> dict:
    state = {}
    # Search Agent Working 
    print("\n" + "="*20 + " Search Agent " + "="*20)
    print(" Searching Agent is working ----")
    print("="*50)

    search_agent = build_search_agent()
    search_results = search_agent.invoke(
        {
            "messages": [("user", 
                          f"Find recent, reliable and detailed information about: {topic}"
                          )]
        }
    )
    state["search_results"] = search_results['messages'][-1].content
    print("Search Agent Results: " + state['search_results'])

    # Reader Agent Working
    print("\n" + "="*20 + " Reader Agent " + "="*20)
    print(" Reader Agent is scraping top results ----")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke(
        {
            "messages":[("user", 
                         f"based on the following search result about '{topic}', "
                         f"pick the most relevant url and scrape it for deeper content.\n\n "
                         f"Search Result: \n{state['search_results'][:800]}"
                         )]
        }
    )
    state["reader_results"] = reader_results['messages'][-1].content
    print("Reader Agent Results: " + state['reader_results'][:200] + "...")

    # Writer Chain Working
    print("\n" + "="*20 + " Writer Chain " + "="*20)
    print(" Writer Chain is generating the research report ----")
    print("="*50)

    research_combined = (f"SEARCCH RESULTS:\n{state['search_results']}\n\n"
                         f"DETAILED SCRAPED CONTENT:\n{state['reader_results']}")
    writer_result = writer_chain.invoke(
        {
            "topic": topic,
            "research": research_combined
        }
    )
    state["report"] = writer_result
    print("Writer Chain Result: " + state['report'][:200] + "...")       

    # Critic Chain Working
    print("\n" + "="*20 + " Critic Chain " + "="*20)
    print(" Critic Chain is evaluating the research report ----")
    print("="*50)

    state['feedback'] = critic_chain.invoke({"report": state['report']})
    print("Critic Chain Feedback: " + state['feedback'][:500] + "...")

    return state

if __name__ == "__main__":
    topic = "Traditional RAG vs Agentic RAG"
    final_state = run_research_pipeline(topic)
    print("\n" + "="*20 + " Final Research Report " + "="*20)
    print(final_state['report']) 

    
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from requests.exceptions import RequestException
load_dotenv()
from rich import print

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable info on a topic and return title, url and snippet result.
    """
    try:
        tavily_response = tavily.search(query, max_results=5)
    except RequestException as exc:
        return f"Search failed: {exc}"
    except Exception as exc:
        return f"Search failed: {exc}"

    out = []
    for r in tavily_response["results"]:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content']}\n")

    return "\n".join(out)


@tool
def web_scraper(url: str) -> str:
    """
    Scrape the content of a webpage and return the text.
    """
    try:
        response = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style','nav','footer','header']):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)[:3000]  # Return first 1000 characters
    except requests.RequestException as e:
        return f"Error fetching the URL: {str(e)}"
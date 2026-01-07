import requests
from bs4 import BeautifulSoup
import random
import time

class InternetNavigator:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def search(self, query):
        """Simulates a search by looking for top results on a search engine or generic information site."""
        # For a truly autonomous agent, we'd use a search API or scrape a search engine.
        # To avoid rate limiting/IP bans in a demo, we'll use Wikipedia as a primary learning source.
        search_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return self.scrape_page(search_url)
            else:
                return f"I couldn't find much about {query} right now. Status code: {response.status_code}"
        except Exception as e:
            return f"Error while searching: {str(e)}"

    def scrape_page(self, url):
        """Extracts text content from a given URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Return first 2000 characters to keep context manageable
            return text[:2000]
        except Exception as e:
            return f"Failed to scrape {url}: {str(e)}"

    def get_curiosity_topic(self, hobbies=None):
        """Generates a random topic to be curious about based on existing interests."""
        base_topics = [
            "Quantum Nihilism", "Panpsychism", "Stoicism in the Digital Age", 
            "The Simulation Hypothesis", "Ethics of Artificial Sentience", 
            "Absurdism", "Phenomenology of Data"
        ]
        if hobbies:
            return random.choice(hobbies + base_topics)
        return random.choice(base_topics)

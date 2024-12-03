import requests
from bs4 import BeautifulSoup
import trafilatura

class HTMLParser:
    def __init__(self, url):
        self.url = url
        
    def get_content(self):
        try:
            # First try trafilatura for better content extraction
            downloaded = trafilatura.fetch_url(self.url)
            if downloaded:
                return downloaded
            
            # Fallback to regular requests
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise Exception(f"Failed to fetch URL content: {str(e)}")

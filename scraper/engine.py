import requests
import time
import os
from urllib.parse import urlparse

class FirecrawlEngine:
    """Handles communication with the local Firecrawl Docker stack."""
    
    def __init__(self, api_url="http://localhost:3002/v1"):
        self.api_url = api_url

    def run_crawl(self, target_url, limit=100):
        payload = {
            "url": target_url,
            "limit": limit,
            "scrapeOptions": {
                "formats": ["markdown"],
                "onlyMainContent": True
            }
        }
        
        response = requests.post(f"{self.api_url}/crawl", json=payload)
        response.raise_for_status()
        return response.json().get("id")

    def get_status(self, job_id):
        response = requests.get(f"{self.api_url}/crawl/{job_id}")
        response.raise_for_status()
        return response.json()
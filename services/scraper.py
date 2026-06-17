import hashlib
import asyncio
import httpx
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

TARGET_FEEDS = [
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml"},
    {"name": "Anthropic News", "url": "https://www.anthropic.com/feed.xml"},
    # Add other RSS/Atom feeds here
]

class NewsScraper:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=15.0,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        
    def generate_content_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def clean_html(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            element.decompose()
            
        text = soup.get_text(separator=" ", strip=True)
        return " ".join(text.split())
    
    async def fetch_article_content(self, url: str) -> str:
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return self.clean_html(response.text)
        except Exception as e:
            logger.warning(f"Failed to fetch content for {url}: {str(e)}")
            return ""
        
    async def process_feed(self, feed_info: dict) -> list[dict]:
        parsed_aricles = []
        try:
            feed = await asyncio.to_thread(feedparser.parse, feed_info["url"])
            
            for entry in feed.entries[:10]:
                link = entry.link
                title = entry.title
                
                cleaned_content = BeautifulSoup(
                    entry.get("summary", ""),
                    "html.parser"
                ).get_text()

                if not cleaned_content:
                    cleaned_content = BeautifulSoup(
                        entry.get("summary", ""),
                        "html.parser"
                    ).get_text()

                if len(cleaned_content) < 50:
                    continue
                content_hash = self.generate_content_hash(cleaned_content)
                
                pub_date = datetime.now(timezone.utc)
                if hasattr(entry, 'pubished_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                    
                parsed_aricles.append({
                    "title": title,
                    "author": entry.get("author", feed_info["name"]),
                    "publication_date": pub_date,
                    "source": feed_info["name"],
                    "url": link,
                    "raw_content": entry.get("summary", ""), # Keep original summary as backup
                    "cleaned_content": cleaned_content,
                    "content_hash": content_hash
                })
        except Exception as e:
            logger.error(f"Error processing feed {feed_info['name']}: {str(e)}")
        return parsed_aricles
    
    async def run_collection_cycle(self) -> list[dict]:
        """Main entry point to fetch from all configured sources."""
        all_articles = []
        tasks = [self.process_feed(feed) for feed in TARGET_FEEDS]
        results = await asyncio.gather(*tasks)
        
        for feed_results in results:
            all_articles.extend(feed_results)
            
        return all_articles

    async def close(self):
        await self.client.aclose()
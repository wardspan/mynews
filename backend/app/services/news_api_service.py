import httpx
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from ..core.config import settings
import uuid

logger = logging.getLogger(__name__)

async def get_articles_from_newsapi(categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Fetch articles from NewsAPI.org"""
    if not settings.NEWSAPI_API_KEY:
        logger.warning("NewsAPI key not configured")
        return []
        
    try:
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        
        # Build query parameters
        params = {
            "apiKey": settings.NEWSAPI_API_KEY,
            "language": "en",
            "from": week_ago.strftime("%Y-%m-%d"),
            "to": today.strftime("%Y-%m-%d"),
            "sortBy": "publishedAt"
        }
        
        # Add category if provided
        if categories and len(categories) > 0:
            # NewsAPI expects a single category
            # We'll use the first relevant one
            valid_categories = ["business", "entertainment", "general", 
                           "health", "science", "sports", "technology"]
            
            for category in categories:
                if category.lower() in valid_categories:
                    params["category"] = category.lower()
                    break
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://newsapi.org/v2/top-headlines",
                params=params,
                timeout=10.0
            )
            
            if response.status_code != 200:
                logger.error(f"NewsAPI error: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            
            if data.get("status") != "ok":
                logger.error(f"NewsAPI returned non-OK status: {data}")
                return []
            
            articles = []
            for item in data.get("articles", []):
                if not item.get("url") or not item.get("title"):
                    continue
                
                # Handle published date properly
                published_date = today.isoformat()
                try:
                    if item.get("publishedAt"):
                        published_date = item.get("publishedAt")
                except Exception as e:
                    logger.warning(f"Error parsing date: {e}")
                
                article = {
                    "id": str(uuid.uuid4()),
                    "title": item.get("title", "Untitled"),
                    "source": item.get("source", {}).get("name", "NewsAPI"),
                    "source_url": item.get("url", ""),
                    "author": item.get("author"),
                    "published_date": published_date,
                    "synopsis": item.get("description", ""),
                    "content": item.get("content", ""),
                    "image_url": item.get("urlToImage"),
                    "categories": categories or [],
                    "ai_tags": [],  # We'll add AI tagging later
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                articles.append(article)
            
            return articles
    except Exception as e:
        logger.exception(f"Error fetching from NewsAPI: {str(e)}")
        return []

async def get_articles(categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Get articles from all configured news sources"""
    # For now, we're just using NewsAPI, but we can add more sources later
    articles = await get_articles_from_newsapi(categories)
    
    # Later we can add more news sources:
    # gnews_articles = await get_articles_from_gnews(categories)
    # guardian_articles = await get_articles_from_guardian(categories)
    # articles.extend(gnews_articles)
    # articles.extend(guardian_articles)
    
    return articles
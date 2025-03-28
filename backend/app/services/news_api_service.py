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

async def get_articles_from_gnews(categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Fetch articles from GNews API"""
    if not settings.GNEWS_API_KEY:
        logger.warning("GNews API key not configured")
        return []
        
    try:
        # Build query parameters
        params = {
            "token": settings.GNEWS_API_KEY,
            "lang": "en",
            "country": "us",
            "max": 10  # Number of results
        }
        
        # Add topic if provided
        if categories and len(categories) > 0:
            # GNews supports topics but limited to predefined ones
            # Map our categories to GNews topics
            gnews_topics = {
                "business": "business",
                "entertainment": "entertainment",
                "health": "health",
                "science": "science",
                "sports": "sports",
                "technology": "technology",
                "world": "world",
                "nation": "nation"
            }
            
            for category in categories:
                category_lower = category.lower()
                if category_lower in gnews_topics:
                    params["topic"] = gnews_topics[category_lower]
                    break
        
        async with httpx.AsyncClient() as client:
            # Use top headlines endpoint
            response = await client.get(
                "https://gnews.io/api/v4/top-headlines",
                params=params,
                timeout=10.0
            )
            
            if response.status_code != 200:
                logger.error(f"GNews API error: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            
            articles = []
            for item in data.get("articles", []):
                if not item.get("url") or not item.get("title"):
                    continue
                
                # Handle published date
                published_date = datetime.utcnow().isoformat()
                try:
                    if item.get("publishedAt"):
                        published_date = item.get("publishedAt")
                except Exception as e:
                    logger.warning(f"Error parsing GNews date: {e}")
                
                article = {
                    "id": str(uuid.uuid4()),
                    "title": item.get("title", "Untitled"),
                    "source": item.get("source", {}).get("name", "GNews"),
                    "source_url": item.get("url", ""),
                    "author": None,  # GNews doesn't provide author info
                    "published_date": published_date,
                    "synopsis": item.get("description", ""),
                    "content": item.get("content", ""),
                    "image_url": item.get("image"),
                    "categories": categories or [],
                    "ai_tags": [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                articles.append(article)
            
            logger.info(f"Retrieved {len(articles)} articles from GNews")
            return articles
    except Exception as e:
        logger.exception(f"Error fetching from GNews API: {str(e)}")
        return []

async def get_articles_from_guardian(categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Fetch articles from The Guardian API"""
    if not settings.GUARDIAN_API_KEY:
        logger.warning("Guardian API key not configured")
        return []
        
    try:
        # Map our categories to Guardian sections
        guardian_sections = {
            "business": "business",
            "technology": "technology",
            "sports": "sport",
            "politics": "politics",
            "science": "science",
            "health": "society",
            "culture": "culture",
            "entertainment": "culture",
            "fashion": "fashion",
            "environment": "environment",
            "world": "world",
        }
        
        # Build query parameters
        params = {
            "api-key": settings.GUARDIAN_API_KEY,
            "show-fields": "headline,byline,thumbnail,trailText,bodyText,publication",
            "page-size": 10,
            "order-by": "newest"
        }
        
        # Add section parameter if relevant categories provided
        if categories and len(categories) > 0:
            sections = []
            for category in categories:
                category_lower = category.lower()
                if category_lower in guardian_sections:
                    sections.append(guardian_sections[category_lower])
            
            if sections:
                params["section"] = "|".join(sections)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://content.guardianapis.com/search",
                params=params,
                timeout=10.0
            )
            
            if response.status_code != 200:
                logger.error(f"Guardian API error: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            
            articles = []
            for item in data.get("response", {}).get("results", []):
                if not item.get("webUrl") or not item.get("webTitle"):
                    continue
                
                fields = item.get("fields", {})
                
                article = {
                    "id": str(uuid.uuid4()),
                    "title": fields.get("headline", item.get("webTitle", "Untitled")),
                    "source": "The Guardian",
                    "source_url": item.get("webUrl", ""),
                    "author": fields.get("byline"),
                    "published_date": item.get("webPublicationDate", datetime.utcnow().isoformat()),
                    "synopsis": fields.get("trailText", ""),
                    "content": fields.get("bodyText", ""),
                    "image_url": fields.get("thumbnail"),
                    "categories": [item.get("sectionName")] + (categories or []),
                    "ai_tags": [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                articles.append(article)
            
            logger.info(f"Retrieved {len(articles)} articles from The Guardian")
            return articles
    except Exception as e:
        logger.exception(f"Error fetching from Guardian API: {str(e)}")
        return []

async def get_articles(categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Get articles from all configured news sources"""
    all_articles = []
    
    # Run all API calls concurrently
    tasks = [
        get_articles_from_newsapi(categories),
        get_articles_from_gnews(categories),
        get_articles_from_guardian(categories)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results, skipping any that raised exceptions
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"Error fetching articles: {str(result)}")
            continue
            
        if isinstance(result, list):
            all_articles.extend(result)
    
    # Remove duplicates based on title similarity
    unique_articles = []
    seen_titles = set()
    
    for article in all_articles:
        title = article.get("title", "").lower()
        # Create a simplified version of the title for comparison
        simple_title = ''.join(c for c in title if c.isalnum()).lower()
        
        if simple_title and simple_title not in seen_titles:
            seen_titles.add(simple_title)
            unique_articles.append(article)
    
    logger.info(f"Retrieved {len(unique_articles)} unique articles from all sources")
    return unique_articles
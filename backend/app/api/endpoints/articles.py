from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import logging

from ...db.base import get_database
from ...schemas.article import Article, ArticleCreate, ArticleInDB
from ...services.news_api_service import get_articles
from ...core.config import settings
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Article])
async def read_articles(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    source: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Retrieve articles with optional filtering.
    """
    try:
        # Build query filter
        filter_query = {}
        
        if category:
            filter_query["categories"] = category
            
        if source:
            filter_query["source"] = source
            
        if search:
            filter_query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"synopsis": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}}
            ]
        
        # Get articles from database
        cursor = db["articles"].find(filter_query).sort("published_date", -1).skip(skip).limit(limit)
        
        articles = await cursor.to_list(length=limit)
        
        # Ensure all articles have required fields
        for article in articles:
            if "title" not in article or not article["title"]:
                article["title"] = "Untitled Article"
            if "source" not in article or not article["source"]:
                article["source"] = "Unknown Source"
            if "source_url" not in article or not article["source_url"]:
                article["source_url"] = "https://example.com"
            if "published_date" not in article:
                article["published_date"] = datetime.utcnow()
            if "synopsis" not in article:
                article["synopsis"] = ""
            if "content" not in article:
                article["content"] = ""
                
        return articles
    except Exception as e:
        logger.exception(f"Error reading articles: {str(e)}")
        return []

@router.get("/latest", response_model=List[Article])
async def get_latest_articles(
    limit: int = 20,
    refresh: bool = False,
    categories: Optional[List[str]] = Query(None),
    sources: Optional[List[str]] = Query(None, description="Filter by news sources (newsapi, gnews, guardian)"),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get the latest articles. Set refresh=true to fetch new articles from sources.
    """
    try:
        if refresh:
            # Fetch new articles from news APIs
            new_articles = await get_articles(categories)
            
            # Filter by source if requested
            if sources:
                source_map = {
                    "newsapi": "NewsAPI",
                    "gnews": "GNews", 
                    "guardian": "The Guardian"
                }
                
                # Convert sources to their display names
                source_display_names = [source_map.get(s.lower(), s) for s in sources]
                
                # Filter articles by source
                new_articles = [
                    article for article in new_articles
                    if article.get("source") in source_display_names
                ]
            
            # Insert new articles if they don't exist
            if new_articles:
                for article in new_articles:
                    try:
                        # Check if article already exists (by source_url)
                        existing = await db["articles"].find_one({"source_url": article["source_url"]})
                        if not existing:
                            # Ensure all required fields exist
                            if "id" not in article:
                                article["id"] = str(uuid.uuid4())
                            if "created_at" not in article:
                                article["created_at"] = datetime.utcnow()
                            if "updated_at" not in article:
                                article["updated_at"] = datetime.utcnow()
                                
                            await db["articles"].insert_one(article)
                    except Exception as e:
                        logger.error(f"Error saving article: {str(e)}")
        
        # Build query for retrieving articles
        filter_query = {}
        
        # Add source filter if requested
        if sources:
            source_map = {
                "newsapi": "NewsAPI",
                "gnews": "GNews", 
                "guardian": "The Guardian"
            }
            source_display_names = [source_map.get(s.lower(), s) for s in sources]
            filter_query["source"] = {"$in": source_display_names}
            
        # Add category filter if requested
        if categories:
            filter_query["categories"] = {"$in": categories}
        
        # Get the latest articles from database
        cursor = db["articles"].find(filter_query).sort("published_date", -1).limit(limit)
        
        articles = await cursor.to_list(length=limit)
        
        # Log the number of articles retrieved
        logger.info(f"Retrieved {len(articles)} articles from database")
        
        return articles
    except Exception as e:
        logger.exception(f"Error in get_latest_articles: {str(e)}")
        # Return empty list instead of raising exception
        return []

@router.get("/{article_id}", response_model=Article)
async def read_article(
    article_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get a specific article by ID.
    """
    try:
        article = await db["articles"].find_one({"id": article_id})
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Ensure all required fields exist
        if "title" not in article or not article["title"]:
            article["title"] = "Untitled Article"
        if "source" not in article or not article["source"]:
            article["source"] = "Unknown Source"
        if "source_url" not in article or not article["source_url"]:
            article["source_url"] = "https://example.com"
        if "published_date" not in article:
            article["published_date"] = datetime.utcnow()
        if "synopsis" not in article:
            article["synopsis"] = ""
        if "content" not in article:
            article["content"] = ""
            
        return article
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching article {article_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=Article)
async def create_article(
    article: ArticleCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a new article (mainly for testing).
    """
    try:
        article_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        article_dict = article.dict()
        
        # Ensure published_date is a string if it's a datetime
        if isinstance(article_dict.get("published_date"), datetime):
            article_dict["published_date"] = article_dict["published_date"].isoformat()
            
        article_in_db = {
            **article_dict,
            "id": article_id,
            "created_at": now,
            "updated_at": now
        }
        
        await db["articles"].insert_one(article_in_db)
        
        return article_in_db
    except Exception as e:
        logger.exception(f"Error creating article: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sources/list", response_model=List[Dict[str, Any]])
async def get_sources():
    """
    Get information about available news sources.
    """
    sources = [
        {
            "id": "newsapi",
            "name": "NewsAPI.org",
            "enabled": bool(settings.NEWSAPI_API_KEY),
            "description": "Provides breaking news headlines and search for articles from over 80,000 sources.",
            "categories": ["business", "entertainment", "general", "health", "science", "sports", "technology"]
        },
        {
            "id": "gnews",
            "name": "GNews API",
            "enabled": bool(settings.GNEWS_API_KEY),
            "description": "Searchable and real-time news data from various sources around the web.",
            "categories": ["business", "entertainment", "health", "science", "sports", "technology", "world", "nation"]
        },
        {
            "id": "guardian",
            "name": "The Guardian",
            "enabled": bool(settings.GUARDIAN_API_KEY),
            "description": "Open platform for accessing Guardian content, providing a rich set of articles.",
            "categories": ["business", "technology", "sport", "politics", "science", "society", "culture", "environment", "world"]
        }
    ]
    
    return sources

@router.get("/categories/list", response_model=List[Dict[str, Any]])
async def get_all_categories():
    """
    Get all available article categories from all sources.
    """
    # Combine categories from all sources
    categories = [
        {"id": "business", "name": "Business", "sources": ["newsapi", "gnews", "guardian"]},
        {"id": "technology", "name": "Technology", "sources": ["newsapi", "gnews", "guardian"]},
        {"id": "entertainment", "name": "Entertainment", "sources": ["newsapi", "gnews"]},
        {"id": "health", "name": "Health", "sources": ["newsapi", "gnews"]},
        {"id": "science", "name": "Science", "sources": ["newsapi", "gnews", "guardian"]},
        {"id": "sports", "name": "Sports", "sources": ["newsapi", "gnews", "guardian"]},
        {"id": "world", "name": "World", "sources": ["gnews", "guardian"]},
        {"id": "politics", "name": "Politics", "sources": ["guardian"]},
        {"id": "environment", "name": "Environment", "sources": ["guardian"]},
        {"id": "culture", "name": "Culture", "sources": ["guardian"]},
    ]
    
    return categories
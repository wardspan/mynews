from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from ...db.base import get_database
from ...schemas.article import Article, ArticleCreate, ArticleInDB
from ...services.news_api_service import get_articles
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/", response_model=List[Article])
async def read_articles(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Retrieve articles with optional category filtering.
    """
    try:
        # Build query filter
        filter_query = {}
        if category:
            filter_query["categories"] = category
        
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
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get the latest articles. Set refresh=true to fetch new articles from sources.
    """
    try:
        if refresh:
            # Fetch new articles from news APIs
            new_articles = await get_articles(categories)
            
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
        
        # Get the latest articles from database
        cursor = db["articles"].find().sort("published_date", -1).limit(limit)
        
        articles = await cursor.to_list(length=limit)
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
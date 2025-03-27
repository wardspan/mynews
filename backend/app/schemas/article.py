from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    source: str
    source_url: str  # Changed from HttpUrl to str to be more flexible
    author: Optional[str] = None
    published_date: Union[datetime, str]  # Accept either datetime or string
    synopsis: Optional[str] = ""
    content: Optional[str] = ""
    image_url: Optional[str] = None  # Changed from HttpUrl to Optional[str]
    categories: List[str] = []
    ai_tags: List[str] = []

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    synopsis: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    categories: Optional[List[str]] = None
    ai_tags: Optional[List[str]] = None

class Article(ArticleBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ArticleInDB(Article):
    pass

class ArticlePublic(Article):
    # This class can be used if we want to hide certain fields from public view
    pass
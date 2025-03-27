from fastapi import APIRouter
from .endpoints import auth, articles 

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])

# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
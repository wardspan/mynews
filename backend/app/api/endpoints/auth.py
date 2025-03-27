from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from typing import Any
from jose import jwt, JWTError
from pydantic import ValidationError

from ...core.config import settings
from ...core.security import create_access_token, verify_password, get_password_hash
from ...db.base import get_database
from ...schemas.user import User, UserCreate, Token, TokenPayload, UserInDB
import uuid
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_database)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await db["users"].find_one({"id": token_data.sub})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInDB(**user)

@router.post("/register", response_model=User)
async def register(user_in: UserCreate, db = Depends(get_database)):
    user = await db["users"].find_one({"email": user_in.email})
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists",
        )
    
    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow()
    
    user_in_db = UserInDB(
        id=user_id,
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password),
        created_at=created_at,
        updated_at=created_at
    )
    
    await db["users"].insert_one(user_in_db.dict())
    
    # Create some default categories for the user
    default_categories = [
        {
            "id": str(uuid.uuid4()),
            "name": "Technology",
            "slug": "technology",
            "user_id": user_id,
            "is_default": True,
            "order": 0,
            "created_at": created_at,
            "updated_at": created_at
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Business",
            "slug": "business",
            "user_id": user_id,
            "is_default": True,
            "order": 1,
            "created_at": created_at,
            "updated_at": created_at
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Science",
            "slug": "science",
            "user_id": user_id,
            "is_default": True,
            "order": 2,
            "created_at": created_at,
            "updated_at": created_at
        }
    ]
    
    if default_categories:
        await db["categories"].insert_many(default_categories)
    
    return User(**user_in_db.dict())

@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_database)
) -> Any:
    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user["id"], expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Union
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "MyNews API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "temporary_secret_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = "mynews"
    
    # CORS
    # We'll handle this as a comma-separated string in the environment
    BACKEND_CORS_ORIGINS: Union[List[str], str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # News APIs
    NEWSAPI_API_KEY: str = os.getenv("NEWSAPI_API_KEY", "")
    GNEWS_API_KEY: str = os.getenv("GNEWS_API_KEY", "")
    GUARDIAN_API_KEY: str = os.getenv("GUARDIAN_API_KEY", "")
    MEDIASTACK_API_KEY: str = os.getenv("MEDIASTACK_API_KEY", "")
    COINGECKO_API_KEY: Optional[str] = os.getenv("COINGECKO_API_KEY", "")
    ALPHAVANTAGE_API_KEY: str = os.getenv("ALPHAVANTAGE_API_KEY", "")
    
    # Cybersecurity APIs
    CYBER_DEFENSE_API_KEY: Optional[str] = os.getenv("CYBER_DEFENSE_API_KEY", "")
    CYBER_SECURITY_API_KEY: Optional[str] = os.getenv("CYBER_SECURITY_API_KEY", "")
    API_SECURITY_API_KEY: Optional[str] = os.getenv("API_SECURITY_API_KEY", "")
    THREAT_INTEL_API_KEY: Optional[str] = os.getenv("THREAT_INTEL_API_KEY", "")
    
    # OpenAI API
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Google Cloud
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    GCP_PROJECT_ID: Optional[str] = os.getenv("GCP_PROJECT_ID", "")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"  # Allow extra fields in the settings

settings = Settings()
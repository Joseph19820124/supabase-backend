from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase 配置
    supabase_url: str = ""
    supabase_key: str = ""
    
    # 应用配置
    app_name: str = "Supabase Backend"
    debug: bool = False
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

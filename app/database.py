from supabase import create_client, Client
from app.config import settings

def get_supabase_client() -> Client:
    """获取 Supabase 客户端实例"""
    if not settings.supabase_url or not settings.supabase_key:
        raise ValueError("Supabase URL and Key must be configured")
    
    return create_client(settings.supabase_url, settings.supabase_key)

# 创建全局客户端实例
supabase: Client = None

def init_supabase():
    """初始化 Supabase 客户端"""
    global supabase
    try:
        supabase = get_supabase_client()
        return supabase
    except Exception as e:
        print(f"Failed to initialize Supabase: {e}")
        return None

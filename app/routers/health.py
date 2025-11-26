from fastapi import APIRouter
from app.database import supabase, init_supabase

router = APIRouter()

@router.get("/health")
async def health_check():
    """健康检查端点"""
    db_status = "disconnected"
    
    try:
        client = init_supabase()
        if client:
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status
    }

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import init_supabase

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    name: str
    avatar_url: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class User(BaseModel):
    id: str
    email: str
    name: str
    avatar_url: Optional[str] = None
    created_at: Optional[str] = None

@router.get("/")
async def get_users():
    """获取所有用户"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        response = supabase.table("users").select("*").execute()
        return {"users": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_user(user_id: str):
    """根据 ID 获取用户"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"user": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_user(user: UserCreate):
    """创建新用户"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        response = supabase.table("users").insert(user.model_dump()).execute()
        return {"user": response.data[0], "message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    """更新用户信息"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        update_data = {k: v for k, v in user.model_dump().items() if v is not None}
        response = supabase.table("users").update(update_data).eq("id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"user": response.data[0], "message": "User updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """删除用户"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        response = supabase.table("users").delete().eq("id", user_id).execute()
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

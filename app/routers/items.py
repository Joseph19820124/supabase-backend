from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import init_supabase

router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    user_id: Optional[str] = None

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

@router.get("/")
async def get_items():
    """获取所有物品"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        response = supabase.table("items").select("*").execute()
        return {"items": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{item_id}")
async def get_item(item_id: str):
    """根据 ID 获取物品"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        response = supabase.table("items").select("*").eq("id", item_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return {"item": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_item(item: ItemCreate):
    """创建新物品"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        response = supabase.table("items").insert(item.model_dump()).execute()
        return {"item": response.data[0], "message": "Item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{item_id}")
async def update_item(item_id: str, item: ItemUpdate):
    """更新物品信息"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        update_data = {k: v for k, v in item.model_dump().items() if v is not None}
        response = supabase.table("items").update(update_data).eq("id", item_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return {"item": response.data[0], "message": "Item updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    """删除物品"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        response = supabase.table("items").delete().eq("id", item_id).execute()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

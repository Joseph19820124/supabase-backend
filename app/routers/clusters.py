from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import init_supabase

router = APIRouter()

class ClusterCreate(BaseModel):
    total_task_number: int
    cluster_name: str

class ClusterUpdate(BaseModel):
    total_task_number: Optional[int] = None
    cluster_name: Optional[str] = None

@router.get("/")
async def get_clusters():
    """获取所有集群"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")

        response = supabase.table("clusters").select("*").execute()
        return {"clusters": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{cluster_id}")
async def get_cluster(cluster_id: str):
    """根据 ID 获取集群"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")

        response = supabase.table("clusters").select("*").eq("id", cluster_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Cluster not found")

        return {"cluster": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_cluster(cluster: ClusterCreate):
    """创建新集群"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")

        response = supabase.table("clusters").insert(cluster.model_dump()).execute()
        return {"cluster": response.data[0], "message": "Cluster created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{cluster_id}")
async def update_cluster(cluster_id: str, cluster: ClusterUpdate):
    """更新集群信息"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")

        update_data = {k: v for k, v in cluster.model_dump().items() if v is not None}
        response = supabase.table("clusters").update(update_data).eq("id", cluster_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Cluster not found")

        return {"cluster": response.data[0], "message": "Cluster updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{cluster_id}")
async def delete_cluster(cluster_id: str):
    """删除集群"""
    try:
        supabase = init_supabase()
        if not supabase:
            raise HTTPException(status_code=500, detail="Database connection failed")

        response = supabase.table("clusters").delete().eq("id", cluster_id).execute()
        return {"message": "Cluster deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

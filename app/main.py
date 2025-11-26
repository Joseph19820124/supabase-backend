from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, users, items, clusters

app = FastAPI(
    title="Supabase Backend API",
    description="A backend API powered by FastAPI and Supabase",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router, tags=["Health"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(items.router, prefix="/api/items", tags=["Items"])
app.include_router(clusters.router, prefix="/api/clusters", tags=["Clusters"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Supabase Backend API",
        "docs": "/docs",
        "health": "/health"
    }

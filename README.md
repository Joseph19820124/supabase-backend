# Supabase Backend

基于 FastAPI + Supabase 的后端 API，可部署到 Railway。

## 技术栈

- **FastAPI** - 现代、快速的 Python Web 框架
- **Supabase** - 开源的 Firebase 替代方案（PostgreSQL 数据库）
- **Railway** - 简单的云部署平台

## 项目结构

```
supabase-backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 应用入口
│   ├── config.py        # 配置管理
│   ├── database.py      # Supabase 连接
│   └── routers/         # API 路由
│       ├── health.py    # 健康检查
│       ├── users.py     # 用户 CRUD
│       └── items.py     # 物品 CRUD
├── requirements.txt     # Python 依赖
├── Procfile            # Railway 启动配置
├── railway.json        # Railway 部署配置
└── .env.example        # 环境变量示例
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Joseph19820124/supabase-backend.git
cd supabase-backend
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 Supabase 配置：

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### 5. 在 Supabase 创建数据表

在 Supabase SQL Editor 中运行：

```sql
-- 创建 users 表
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建 items 表
CREATE TABLE items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 启用 RLS (Row Level Security)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- 创建允许所有操作的策略（开发用，生产环境应该更严格）
CREATE POLICY "Allow all" ON users FOR ALL USING (true);
CREATE POLICY "Allow all" ON items FOR ALL USING (true);
```

### 6. 运行开发服务器

```bash
uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档。

## 部署到 Railway

### 方法一：通过 GitHub 连接

1. 登录 [Railway](https://railway.app)
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择此仓库
4. 添加环境变量：
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
5. 部署完成！

### 方法二：使用 Railway CLI

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 部署
railway up
```

## API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | 欢迎页面 |
| GET | `/health` | 健康检查 |
| GET | `/api/users` | 获取所有用户 |
| GET | `/api/users/{id}` | 获取单个用户 |
| POST | `/api/users` | 创建用户 |
| PUT | `/api/users/{id}` | 更新用户 |
| DELETE | `/api/users/{id}` | 删除用户 |
| GET | `/api/items` | 获取所有物品 |
| GET | `/api/items/{id}` | 获取单个物品 |
| POST | `/api/items` | 创建物品 |
| PUT | `/api/items/{id}` | 更新物品 |
| DELETE | `/api/items/{id}` | 删除物品 |

## 许可证

MIT

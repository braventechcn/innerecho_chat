from fastapi import FastAPI     # 导入 FastAPI 主类
# 导入 CORS 中间件以处理跨域请求
from fastapi.middleware.cors import CORSMiddleware # CORS（跨域资源共享）用于允许前端（如 React/Vue）在不同域名/端口下访问后端 API
# 导入自定义的中间件（如日志中间件）
from backend.middleware.logging_middleware import LoggingMiddleware
# 导入自定义的路由模块（router），每个模块负责一类 API 路由（如聊天、记忆、反馈等）
from backend.routers import agent_router, chat, evaluation, feedback, memory

# 创建 FastAPI 应用实例，设置标题和版本号
app = FastAPI(title="InnerEcho API", version="0.1.0")

# 设置 CORS 中间件，允许所有来源访问 API
# - CORS 中间件常见用途：日志、鉴权、异常捕获、限流等
# - 所有请求和响应都会经过 CORS 中间件，自动加上允许跨域的 HTTP 头
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)
app.add_middleware(LoggingMiddleware) # 添加日志中间件

# 注册各个功能模块的路由到主应用，把 router 里所有的路由都统一加上 /api 前缀
# - 例如，聊天相关接口会变成 /api/chat/...
app.include_router(chat.router, prefix="/api")
app.include_router(agent_router.router, prefix="/api")
app.include_router(memory.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(evaluation.router, prefix="/api")

# 定义 /health 路由，返回服务健康状态。常用于部署时的健康检查（K8s、云平台等）
@app.get("/health")
def healthcheck() -> dict:
    """Lightweight liveness probe."""
    return {"status": "ok"}

# 定义根路径 /，返回服务名和版本号，便于快速验证 API 是否正常启动
@app.get("/")
def root() -> dict:
    """Surface a simple landing payload for quick verification."""
    return {"service": "InnerEcho API", "version": "0.1.0"}

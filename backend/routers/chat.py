"""
Chat router for handling chat-related endpoints.
Chat 相关的 API 路由模块，负责接收前端请求，调用服务层处理，并返回响应

路由层的主要职责是：
 - 接收前端请求
 - 校验和解析请求参数
 - 调用服务层处理业务逻辑
 - 返回结构化响应
 - 处理异常并返回友好错误码
"""

# 导入 FastAPI 路由相关类和异常处理类
# - FastAPI 推荐用 APIRouter 将不同功能的接口分模块管理，便于维护和扩展
# - FastAPI 推荐用 HTTPException 抛出 HTTP 错误码，前端可据此做友好提示
from fastapi import APIRouter, Body, HTTPException

# 导入 Pydantic 的数据模型和字段描述工具
# - FastAPI 用 Pydantic 进行请求参数和响应数据的自动校验和序列化。
# - BaseModel 定义数据结构和类型约束，Field 可设置描述、默认值、校验规则等
from pydantic import BaseModel, Field

# 导入聊天服务层，负责实际业务逻辑处理（如调用大模型 API）
from backend.services.chat_service import ChatService

# 创建一个路由分组实例
# - 路由可以设置前缀（如 /chat），所有接口都自动带上这个前缀
router = APIRouter(prefix="/chat", tags=["chat"])
# 实例化聊天服务对象，后续接口会用它处理业务逻辑
chat_service = ChatService()

# 定义请求体的数据结构，继承自 Pydantic 的 BaseModel
# - user_id：用户唯一标识，必填。
# - message：用户输入文本，必填且至少1个字符。
# - Field 用于描述字段和设置校验规则
class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    message: str = Field(..., min_length=1, description="User input text")

# 定义响应体的数据结构
# - 包含用户ID、原始消息、模型回复、模型名称和延迟（毫秒）
class ChatResponse(BaseModel):
    user_id: str
    message: str
    reply: str
    model: str
    latency_ms: float


# 定义一个 POST 接口 /chat/message，用于接收前端的请求体，调用服务层处理，并返回响应
@router.post("/message", response_model=ChatResponse)
def post_message(payload: ChatRequest = Body(...)) -> ChatResponse:
    """
    Send a message to the chat service and return the model reply.
    Args:
        payload: ChatRequest 包含 user_id 和 message 字段的请求体（请求体必须符合 ChatRequest 结构，自动校验）
    Returns:
        ChatResponse 包含用户ID、原始消息、模型回复、模型名称和延迟（毫秒）
    """

    try:
        # 自动将返回值序列化为响应体结构，并生成接口文档
        return chat_service.send_message(payload.user_id, payload.message)  # type: ignore[return-value]
    except Exception as exc:  # Surface as HTTP 502 for client clarity
        # 如果服务层抛出异常（如模型API错误、网络异常），则返回 HTTP 502 错误码，并附带错误详情，便于前端做友好提示
        raise HTTPException(status_code=502, detail=str(exc)) from exc

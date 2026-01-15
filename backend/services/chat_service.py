"""
Chat service layer for orchestrating chat flows.
服务层负责业务编排和性能统计，不关心底层 HTTP 细节，只关心输入输出和异常处理
"""

from __future__ import annotations

import time

from config import Config
from backend.modules.llm.qwen_client import QwenClient


class ChatService:
    """
    Handle chat messages and forward them to the model backend.
    聊天服务的业务逻辑层，负责接收用户消息，调用大模型客户端，并返回结构化的回复
    """

    def __init__(self) -> None:
        self.client = QwenClient(
            api_key=Config.DASHSCOPE_API_KEY or "",
            base_url=Config.API_BASE_URL,
            default_model=Config.DEFAULT_MODEL,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
        )

    def send_message(self, user_id: str, message: str) -> dict:
        """Send a user message to the model and return structured metadata."""

        start = time.perf_counter() # 记录请求开始时间
        # 调用 QwenClient 发送消息并获取回复文本
        reply_text = self.client.generate(message)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2) # 计算请求耗时，单位毫秒

        return {
            "user_id": user_id,
            "message": message,
            "reply": reply_text,
            "model": self.client.default_model,
            "latency_ms": elapsed_ms,
        }

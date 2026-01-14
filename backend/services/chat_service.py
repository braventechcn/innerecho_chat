"""Chat service layer for orchestrating chat flows."""

from __future__ import annotations

import time

from config import Config
from backend.modules.llm.qwen_client import QwenClient


class ChatService:
    """Handle chat messages and forward them to the model backend."""

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

        start = time.perf_counter()
        reply_text = self.client.generate(message)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "user_id": user_id,
            "message": message,
            "reply": reply_text,
            "model": self.client.default_model,
            "latency_ms": elapsed_ms,
        }

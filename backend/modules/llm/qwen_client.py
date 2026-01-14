"""Lightweight Qwen client stub."""

class QwenClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key
        self.base_url = base_url

    def generate(self, prompt: str, **kwargs) -> str:
        """Call Qwen model (stub)."""
        raise NotImplementedError("Qwen generation not implemented")

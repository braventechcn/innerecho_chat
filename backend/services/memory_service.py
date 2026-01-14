"""Memory service layer for storing and retrieving conversations."""

class MemoryService:
    def save_memory(self, user_id: str, content: dict) -> None:
        """Persist conversation memory (stub)."""
        raise NotImplementedError("Memory persistence not implemented")

    def load_memory(self, user_id: str) -> dict:
        """Load stored memory (stub)."""
        raise NotImplementedError("Memory retrieval not implemented")

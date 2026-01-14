"""Chat service layer for orchestrating chat flows."""

class ChatService:
    def send_message(self, user_id: str, message: str) -> dict:
        """Placeholder chat handler."""
        return {"user_id": user_id, "echo": message}

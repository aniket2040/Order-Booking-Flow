from __future__ import annotations
from models import ChatResponse
import requests

from config import (
    BACKEND_URL,
    CUSTOMER_ID,
    SESSION_ID,
)


class ChatAPI:
    """
    Handles communication with the FastAPI backend.
    """

    def __init__(self) -> None:
        self.backend_url = BACKEND_URL
        self.customer_id = CUSTOMER_ID
        self.session_id = SESSION_ID

    def send_message(
        self,
        message: str,
    ) -> dict:
        """
        Send a chat message to the backend.
        """

        response = requests.post(
            self.backend_url,
            json={
                "customer_id": self.customer_id,
                "session_id": self.session_id,
                "message": message,
            },
            timeout=30,
        )

        response.raise_for_status()

        return ChatResponse.from_dict(
            response.json()
        )
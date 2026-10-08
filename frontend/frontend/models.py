from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# ------------------------------------------------------------------
# Payload Types
# ------------------------------------------------------------------

class PayloadType:
    PRODUCT_SELECTION = "PRODUCT_SELECTION"


# ------------------------------------------------------------------
# Chat Message
# ------------------------------------------------------------------

@dataclass
class ChatMessage:
    role: str
    content: str


# ------------------------------------------------------------------
# Backend Response
# ------------------------------------------------------------------

@dataclass
class ChatResponse:
    success: bool
    message: str
    current_state: str
    next_state: str
    payload: dict[str, Any] | None
    review: dict[str, Any] | None
    order_id: str | None

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ChatResponse":

        return cls(
            success=data.get("success", False),
            message=data.get("message", ""),
            current_state=data.get("current_state", ""),
            next_state=data.get("next_state", ""),
            payload=data.get("payload"),
            review=data.get("review"),
            order_id=data.get("order_id"),
        )
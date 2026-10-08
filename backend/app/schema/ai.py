from __future__ import annotations

from typing import Any

from pydantic import Field

from app.models.enums import IntentType
from app.schema.common import BaseSchema


class IntentExtractionResult(BaseSchema):
    """
    Result returned by the intent extractor.
    """

    intent: IntentType = IntentType.UNKNOWN

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    reasoning: str | None = None


class SlotExtractionResult(BaseSchema):
    """
    Structured information extracted
    from the customer's message.
    """

    product: str | None = None

    quantity: int | None = None

    color: str | None = None

    size: str | None = None

    brand: str | None = None

    address: str | None = None

    city: str | None = None

    state: str | None = None

    postal_code: str | None = None

    country: str | None = None

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


class AIResponse(BaseSchema):
    """
    Complete AI response returned by
    the AI pipeline.
    """

    intent: IntentExtractionResult

    slots: SlotExtractionResult
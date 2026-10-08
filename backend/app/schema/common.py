from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Base Schema
# ============================================================

class BaseSchema(BaseModel):
    """
    Base schema for all application DTOs.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="forbid",
        validate_assignment=True,
    )


# ============================================================
# Generic API Response
# ============================================================

T = TypeVar("T")


class ApiResponse(BaseSchema, Generic[T]):
    """
    Generic API response wrapper.
    """

    success: bool = True
    message: str
    data: T | None = None


# ============================================================
# Error Response
# ============================================================

class ErrorResponse(BaseSchema):
    """
    Standard API error response.
    """

    success: bool = False
    error_code: str
    message: str
    details: dict[str, Any] | None = None


# ============================================================
# Message Response
# ============================================================

class MessageResponse(BaseSchema):
    """
    Simple success response.
    """

    success: bool = True
    message: str

class ValidationResult(BaseSchema):
    """
    Represents the result of a validation operation.
    """

    valid: bool
    message: str | None = None
    field: str | None = None


# ============================================================
# Pagination
# ============================================================

class Pagination(BaseSchema):
    """
    Pagination metadata.
    """

    page: int = Field(..., ge=1)

    page_size: int = Field(..., ge=1)

    total_records: int = Field(..., ge=0)

    total_pages: int = Field(..., ge=0)


# ============================================================
# Timestamp
# ============================================================

class TimestampSchema(BaseSchema):
    """
    Common timestamp fields.
    """

    created_at: datetime

    updated_at: datetime
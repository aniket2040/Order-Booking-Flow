from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import Field

from app.models.enums import IntentType, WorkflowState, WorkflowMode
from app.schema.common import BaseSchema
from app.schema.review import OrderReview


# ============================================================
# Workflow Request
# ============================================================

class WorkflowRequest(BaseSchema):
    """
    Input received by the Workflow Engine.
    """

    customer_id: UUID

    session_id: UUID

    message: str = Field(
        ...,
        min_length=1,
    )




# ============================================================
# Workflow Context
# ============================================================

class WorkflowContext(BaseSchema):
    """
    Runtime context shared across workflow handlers.
    """

    customer_id: UUID

    session_id: UUID

    workflow_state: WorkflowState
    workflow_mode: WorkflowMode
    intent: IntentType | None = None,

    draft_id: UUID | None = None

    slots: dict[str, Any] = Field(
        default_factory=dict,
    )

    modified_fields: set[str] = Field(
        default_factory=set,
    )


# ============================================================
# Workflow Result
# ============================================================

class WorkflowResult(BaseSchema):

    success: bool = True

    message: str

    next_state: WorkflowState

    payload: dict[str, Any] | None = None

    continue_processing: bool = False

    order_review: OrderReview | None = None

    order_id: UUID | None = None

# ============================================================
# Workflow Response
# ============================================================

class WorkflowResponse(BaseSchema):
    """
    Final response returned to the API layer.
    """

    success: bool

    message: str

    current_state: WorkflowState

    next_state: WorkflowState | None = None

    payload: dict[str, Any] | None = None

    review: OrderReview | None = None

    order_id: UUID | None = None
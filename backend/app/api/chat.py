from __future__ import annotations
from uuid import UUID

from app.Services.draft.draft_service import DraftService
from app.dependencies.service import (
    get_conversation_service, get_draft_service,
)
from app.Services.conversation.conversation_service import (
    ConversationService,
)
from fastapi import APIRouter, Depends, HTTPException, status

from app.Services.conversation import conversation_service
from app.dependencies.workflow import get_workflow_service
from app.exceptions.customer import CustomerNotFoundError
from app.models.enums import WorkflowState
from app.schema.workflow import (
    WorkflowRequest,
    WorkflowResponse, WorkflowContext,
)
from app.Services.workflow.workflow_service import WorkflowService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=WorkflowResponse,
    status_code=status.HTTP_200_OK,
)
async def chat(
    request: WorkflowRequest,
    workflow_service: WorkflowService = Depends(
        get_workflow_service,
    ),
    conversation_service: ConversationService = Depends(
        get_conversation_service,
    ),
    draft_service: DraftService = Depends(
        get_draft_service
    )
):
    try:
        print("===== CHAT START =====")
        message = request.message.lower()

        new_order_keywords = (
            "buy",
            "order",
            "purchase",
            "want",
            "nike",
            "adidas",
            "iphone",
            "samsung",
        )

        
        context = await conversation_service.load_workflow_context(
            customer_id=request.customer_id,
            session_id=request.session_id,
        )

    except CustomerNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Customer not found.",
        )
    print("Context loaded")

    response = await workflow_service.process(
        request,
        context,
    )
    print("Workflow finished")
    print("Response next state:", response.next_state)
    draft = await draft_service.get_by_id(
        context.draft_id,
    )

    await draft_service.update_workflow(
        draft,
        response.next_state,
    )

    await draft_service.update_workflow_mode(
        draft,
        context.workflow_mode,
    )


    print("Session after save:", response.next_state)

    return response





@router.get(
    "/history/{session_id}",
)
async def get_history(
    session_id: UUID,
    conversation_service: ConversationService = Depends(
        get_conversation_service,
    ),
):
    """
    Retrieve conversation history.
    """

    return await conversation_service.get_conversation_history(
        session_id
    )
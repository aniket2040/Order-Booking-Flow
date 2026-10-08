from __future__ import annotations


from fastapi import Depends

from app.ai import prompt_builder, response_parser, slot_extractor
from app.dependencies.service import (
    get_customer_service,
    get_draft_service,
    get_inventory_service,
    get_notification_service,
    get_order_orchestrator,
    get_pricing_service,
    get_product_service,
    get_summary_builder,
    get_validation_service,
)

from app.ai.prompt_builder import PromptBuilder
from app.ai.response_parser import ResponseParser
from app.ai.slot_extractor import SlotExtractor
from app.Services.response.response_builder import ResponseBuilder
from app.Services.payload.payload_builder import PayloadBuilder



from app.Services.customer.customer_service import CustomerService
from app.Services.draft.draft_service import DraftService
from app.Services.inventory.inventory_service import InventoryService

from app.Services.orchestrator.order_orchestrator import (
    OrderOrchestrator,
)
from app.Services.pricing.pricing_service import PricingService
from app.Services.catalog.product_service import ProductService
from app.Services.review.summary_builder import SummaryBuilder
from app.Services.validation.validation_service import ValidationService

from app.Services.workflow.handler_registry import HandlerRegistry
from app.Services.workflow.workflow_service import WorkflowService

from app.Services.workflow.handlers.detect_intent import (
    DetectIntentHandler,
)
from app.Services.workflow.handlers.collect_requirements import (
    CollectRequirementsHandler,
)
from app.Services.workflow.handlers.resolve_product import (
    ResolveProductHandler,
)
from app.Services.workflow.handlers.resolve_variant import (
    ResolveVariantHandler,
)
from app.Services.workflow.handlers.check_availability import (
    CheckAvailabilityHandler,
)
from app.Services.workflow.handlers.collect_address import (
    CollectAddressHandler,
)
from app.Services.workflow.handlers.calculate_pricing import (
    CalculatePricingHandler,
)
from app.Services.workflow.handlers.review_order import (
    ReviewOrderHandler,
)
from app.Services.workflow.handlers.confirm_order import (
    ConfirmOrderHandler,
)
from app.Services.workflow.handlers.create_order import (
    CreateOrderHandler,
)
from app.models.enums import WorkflowState

def get_response_builder() -> ResponseBuilder:
    return ResponseBuilder()


def get_payload_builder() -> PayloadBuilder:
    return PayloadBuilder()


def get_handler_registry(

    product_service: ProductService = Depends(
        get_product_service,
    ),

    inventory_service: InventoryService = Depends(
        get_inventory_service,
    ),

    customer_service: CustomerService = Depends(
        get_customer_service,
    ),

    validation_service: ValidationService = Depends(
        get_validation_service,
    ),

    pricing_service: PricingService = Depends(
        get_pricing_service,
    ),

    draft_service: DraftService = Depends(
        get_draft_service,
    ),

    summary_builder: SummaryBuilder = Depends(
        get_summary_builder,
    ),

    order_orchestrator: OrderOrchestrator = Depends(
        get_order_orchestrator,
    ),

) -> HandlerRegistry:

    registry = HandlerRegistry()
    response_builder = get_response_builder()
    payload_builder = get_payload_builder()
    prompt_builder = PromptBuilder()

    response_parser = ResponseParser()

    slot_extractor = SlotExtractor(
        prompt_builder=prompt_builder,
        response_parser=response_parser,
    )

    registry.register(
        WorkflowState.DETECT_INTENT,
        DetectIntentHandler()
    )



    registry.register(
        WorkflowState.COLLECT_REQUIREMENTS,
        CollectRequirementsHandler(
            validation_service = validation_service,
            draft_service= draft_service,
            slot_extractor=slot_extractor,
            response_builder=response_builder,
        )
    )

    registry.register(
        WorkflowState.RESOLVE_PRODUCT,
        ResolveProductHandler(
            product_service=product_service,
            draft_service=draft_service,
            response_builder=response_builder,
            payload_builder=payload_builder,
        )
    )

    registry.register(
        WorkflowState.RESOLVE_VARIANT,
        ResolveVariantHandler(
            product_service=product_service,
            draft_service=draft_service,
            response_builder=response_builder,
            payload_builder=payload_builder,
        )
    )

    registry.register(
        WorkflowState.CHECK_AVAILABILITY,
        CheckAvailabilityHandler(
            inventory_service=inventory_service,
            response_builder=response_builder,
            payload_builder=payload_builder,
        )
    )

    registry.register(
        WorkflowState.COLLECT_ADDRESS,
        CollectAddressHandler(
            customer_service=customer_service,
            validation_service=validation_service,
            draft_service=draft_service,
            response_builder=response_builder,
            payload_builder=payload_builder,
        )
    )

    registry.register(
        WorkflowState.CALCULATE_PRICING,
        CalculatePricingHandler(
            draft_service=draft_service,
            pricing_service=pricing_service,
            response_builder=response_builder,
        )
    )

    registry.register(
        WorkflowState.REVIEW_ORDER,
        ReviewOrderHandler(
            draft_service=draft_service,
            customer_service=customer_service,
            summary_builder=summary_builder,
            response_builder=response_builder,
        )
    )

    registry.register(
        WorkflowState.CONFIRM_ORDER,
        ConfirmOrderHandler(
        )
    )

    registry.register(
        WorkflowState.CREATE_ORDER,
        CreateOrderHandler(
            draft_service,
            order_orchestrator,
        )
    )

    return registry

def get_workflow_service(
    registry: HandlerRegistry = Depends(
        get_handler_registry,
    ),
) -> WorkflowService:

    return WorkflowService(
        registry,
    )


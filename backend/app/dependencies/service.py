from __future__ import annotations

from fastapi import Depends

from app.Services.response.response_builder import ResponseBuilder
from app.dependencies.repositories import (
    get_address_repository,
    get_customer_repository,
    get_draft_repository,
    get_inventory_repository,
    get_message_repository,
    get_order_repository,
    get_payment_repository,
    get_product_repository,
    get_session_repository,
)

from app.repositories.catalog.inventory_repository import (
    InventoryRepository,
)
from app.repositories.catalog.product_repository import (
    ProductRepository,
)
from app.repositories.conversation.message_repository import (
    MessageRepository,
)
from app.repositories.conversation.session_repository import (
    SessionRepository,
)
from app.repositories.customer.address_repository import (
    AddressRepository,
)
from app.repositories.customer.customer_repository import (
    CustomerRepository,
)
from app.repositories.draft.draft_repository import (
    DraftRepository,
)
from app.repositories.order.order_repository import (
    OrderRepository,
)
from app.repositories.order.payment_repository import (
    PaymentRepository,
)

from app.Services.inventory.inventory_service import (
    InventoryService,
)
from app.Services.catalog.product_service import (
    ProductService,
)
from app.Services.conversation.conversation_service import (
    ConversationService,
)
from app.Services.customer.customer_service import (
    CustomerService,
)
from app.Services.draft.draft_service import (
    DraftService,
)
from app.Services.notification.notification_service import (
    NotificationService,
)
from app.Services.order.order_service import (
    OrderService,
)
from app.Services.orchestrator.order_orchestrator import (
    OrderOrchestrator,
)
from app.Services.payment.payment_service import (
    PaymentService,
)
from app.Services.pricing.pricing_service import (
    PricingService,
)
from app.Services.review.summary_builder import (
    SummaryBuilder,
)
from app.Services.validation.validation_service import (
    ValidationService,
)


def get_product_service(
    repository: ProductRepository = Depends(
        get_product_repository,
    ),
) -> ProductService:

    return ProductService(repository)


def get_inventory_service(
    repository: InventoryRepository = Depends(
        get_inventory_repository,
    ),
) -> InventoryService:

    return InventoryService(repository)


def get_customer_service(
    customer_repository: CustomerRepository = Depends(
        get_customer_repository,
    ),
    address_repository: AddressRepository = Depends(
        get_address_repository,
    ),
) -> CustomerService:

    return CustomerService(
        customer_repository,
        address_repository,
    )




def get_pricing_service() -> PricingService:

    return PricingService()



def get_draft_service(
    repository: DraftRepository = Depends(
        get_draft_repository,
    ),
    pricing_service: PricingService = Depends(
        get_pricing_service,
    ),
) -> DraftService:

    return DraftService(
        repository,
        pricing_service,
    )


def get_order_service(
    repository: OrderRepository = Depends(
        get_order_repository,
    ),
    pricing_service: PricingService = Depends(
        get_pricing_service,
    ),
) -> OrderService:

    return OrderService(
        repository,
        pricing_service,
    )


def get_payment_service(
    repository: PaymentRepository = Depends(
        get_payment_repository,
    ),
) -> PaymentService:

    return PaymentService(
        repository,
    )


def get_validation_service() -> ValidationService:

    return ValidationService()

def get_summary_builder() -> SummaryBuilder:

    return SummaryBuilder()


def get_notification_service() -> NotificationService:

    return NotificationService()

def get_response_builder():
    return ResponseBuilder()

def get_order_orchestrator(
    inventory_service: InventoryService = Depends(
        get_inventory_service,
    ),
    order_service: OrderService = Depends(
        get_order_service,
    ),
    payment_service: PaymentService = Depends(
        get_payment_service,
    ),
    notification_service: NotificationService = Depends(
        get_notification_service,
    ),
    draft_service: DraftService = Depends(
        get_draft_service,
    ),
) -> OrderOrchestrator:

    return OrderOrchestrator(
        inventory_service,
        order_service,
        payment_service,
        notification_service,
        draft_service,
    )

def get_draft_service(
    repository: DraftRepository = Depends(
        get_draft_repository,
    ),
    pricing_service: PricingService = Depends(
        get_pricing_service,
    ),
) -> DraftService:

    return DraftService(
        repository,
        pricing_service,
    )

def get_conversation_service(
    session_repository: SessionRepository = Depends(
        get_session_repository,
    ),
    message_repository: MessageRepository = Depends(
        get_message_repository,
    ),
    draft_service: DraftService = Depends(
        get_draft_service,
    ),
    customer_service: CustomerService = Depends(
        get_customer_service,
    ),
) -> ConversationService:

    return ConversationService(
        session_repository,
        message_repository,
        draft_service,
        customer_service,
    )
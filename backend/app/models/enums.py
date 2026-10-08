from enum import Enum


# ==========================================================
# Conversation
# ==========================================================

class ConversationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"


# ==========================================================
# Workflow Mode
# ==========================================================

class WorkflowMode(str, Enum):
    """
    Indicates whether the workflow
    is creating a new order or
    modifying an existing one.
    """

    NEW_ORDER = "NEW_ORDER"

    MODIFY_ORDER = "MODIFY_ORDER"




class WorkflowState(str, Enum):
    """
    Workflow engine states.
    """

    DETECT_INTENT = "DETECT_INTENT"

    COLLECT_REQUIREMENTS = "COLLECT_REQUIREMENTS"

    RESOLVE_PRODUCT = "RESOLVE_PRODUCT"

    RESOLVE_VARIANT = "RESOLVE_VARIANT"

    CHECK_AVAILABILITY = "CHECK_AVAILABILITY"

    COLLECT_ADDRESS = "COLLECT_ADDRESS"

    CALCULATE_PRICING = "CALCULATE_PRICING"

    REVIEW_ORDER = "REVIEW_ORDER"

    CONFIRM_ORDER = "CONFIRM_ORDER"

    CREATE_ORDER = "CREATE_ORDER"

    ORDER_CONFIRMED = "ORDER_CONFIRMED"

    POST_ORDER_ASSISTANCE = "POST_ORDER_ASSISTANCE"

    END = "END"


class IntentType(str, Enum):
    """
    High-level user intent.
    """

    PLACE_ORDER = "PLACE_ORDER"

    MODIFY_ORDER = "MODIFY_ORDER"

    CONFIRM_ORDER = "CONFIRM_ORDER"

    CANCEL_ORDER = "CANCEL_ORDER"

    UNKNOWN = "UNKNOWN"


class WorkflowAction(str, Enum):
    """
    Customer action while progressing
    through the workflow.
    """

    CONTINUE = "CONTINUE"

    MODIFY = "MODIFY"

    CONFIRM = "CONFIRM"

    CANCEL = "CANCEL"

    RETRY = "RETRY"


# ==========================================================
# Conversation Messages
# ==========================================================

class MessageRole(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"


# ==========================================================
# Draft
# ==========================================================

class DraftStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"
    EXPIRED = "EXPIRED"


# ==========================================================
# Orders
# ==========================================================

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    PACKED = "PACKED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    PROCESSING = "PROCESSING"


# ==========================================================
# Payment
# ==========================================================

class PaymentMethod(str, Enum):
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# ==========================================================
# Shipment
# ==========================================================

class ShipmentStatus(str, Enum):
    PENDING = "PENDING"
    PACKED = "PACKED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
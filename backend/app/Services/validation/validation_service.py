from __future__ import annotations

from app.models.enums import WorkflowState
from app.schema.common import ValidationResult


class ValidationService:
    """
    Handles common business input validations.
    """

    # ---------------------------------------------------------
    # Quantity
    # ---------------------------------------------------------

    def validate_quantity(
        self,
        quantity: int,
    ) -> ValidationResult:

        if quantity <= 0:
            return ValidationResult(
                valid=False,
                field="quantity",
                message="Quantity must be greater than zero.",
            )

        return ValidationResult(valid=True)

    # ---------------------------------------------------------
    # Address
    # ---------------------------------------------------------

    def validate_address(
        self,
        address: str,
    ) -> ValidationResult:

        if not address.strip():

            return ValidationResult(
                valid=False,
                field="address",
                message="Delivery address is required.",
            )

        return ValidationResult(valid=True)

    # ---------------------------------------------------------
    # Required Fields
    # ---------------------------------------------------------

    def validate_required_fields(
        self,
        required_fields: list[str],
        slots: dict,
    ) -> ValidationResult:

        missing = [
            field
            for field in required_fields
            if not slots.get(field)
        ]

        if missing:

            return ValidationResult(
                valid=False,
                field=", ".join(missing),
                message=f"Missing required field(s): {', '.join(missing)}",
            )

        return ValidationResult(valid=True)

    # ---------------------------------------------------------
    # Workflow Transition
    # ---------------------------------------------------------

    def validate_workflow_transition(
        self,
        current_state: WorkflowState,
        next_state: WorkflowState,
    ) -> ValidationResult:

        if current_state == next_state:

            return ValidationResult(
                valid=False,
                field="workflow_state",
                message="Invalid workflow transition.",
            )

        return ValidationResult(valid=True)
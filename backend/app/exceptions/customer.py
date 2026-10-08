from __future__ import annotations

from uuid import UUID


class CustomerNotFoundError(Exception):
    """
    Raised when a customer
    does not exist.
    """

    def __init__(
        self,
        customer_id: UUID,
    ) -> None:

        self.customer_id = customer_id

        super().__init__(
            f"Customer '{customer_id}' not found."
        )
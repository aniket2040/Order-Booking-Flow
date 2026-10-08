from __future__ import annotations

from uuid import UUID

from app.models.customer.address import Address
from app.models.customer.customer import Customer
from app.repositories.customer.address_repository import AddressRepository
from app.repositories.customer.customer_repository import CustomerRepository


class CustomerService:
    """
    Handles customer-related business operations.
    """

    def __init__(
        self,
        customer_repository: CustomerRepository,
        address_repository: AddressRepository,
    ) -> None:

        self.customer_repository = customer_repository
        self.address_repository = address_repository

    # ------------------------------------------------------------------
    # Customer
    # ------------------------------------------------------------------
    async def get_by_id(
            self,
            customer_id: UUID,
    ):
        """
        Retrieve a customer by ID.
        """

        return await self.customer_repository.get_by_id(
            customer_id,
        )


    async def get_customer(
        self,
        customer_id: UUID,
    ) -> Customer | None:
        """
        Get customer by ID.
        """

        return await self.customer_repository.get_by_id(
            customer_id
        )

    async def get_customer_by_email(
        self,
        email: str,
    ) -> Customer | None:
        """
        Get customer by email.
        """

        return await self.customer_repository.get_by_email(
            email
        )

    async def get_customer_by_phone(
        self,
        phone: str,
    ) -> Customer | None:
        """
        Get customer by phone.
        """

        return await self.customer_repository.get_by_phone(
            phone
        )

    async def create_customer(
        self,
        customer: Customer,
    ) -> Customer:
        """
        Create a new customer.
        """

        return await self.customer_repository.create(
            customer
        )

    # ------------------------------------------------------------------
    # Address
    # ------------------------------------------------------------------

    async def get_default_address(
        self,
        customer_id: UUID,
    ) -> Address | None:
        """
        Get customer's default address.
        """

        return await self.address_repository.get_default_address(
            customer_id
        )

    async def get_customer_addresses(
        self,
        customer_id: UUID,
    ) -> list[Address]:
        """
        Get all customer addresses.
        """

        return await self.address_repository.get_customer_addresses(
            customer_id
        )

    async def get_default_address(
            self,
            customer_id: UUID,
    ) -> Address | None:
        """
        Return the customer's default address.
        """

        return await self.address_repository.get_default_address(
            customer_id,
        )

    async def save_address(
            self,
            customer_id: UUID,
            address: dict,
    ) -> Address:
        """
        Create and save a customer address.
        """

        new_address = Address(
            customer_id=customer_id,
            address_line1=address["address_line1"],
            address_line2=address.get("address_line2"),
            city=address["city"],
            state=address["state"],
            country=address["country"],
            postal_code=address["postal_code"],
            is_default=address.get("is_default", True),
        )

        return await self.address_repository.create(
            new_address
        )
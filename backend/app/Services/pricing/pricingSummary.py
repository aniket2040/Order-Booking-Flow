from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class PricingSummary:

    subtotal: Decimal

    tax: Decimal

    shipping_charge: Decimal

    discount: Decimal

    grand_total: Decimal
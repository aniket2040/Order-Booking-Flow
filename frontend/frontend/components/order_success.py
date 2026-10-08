from __future__ import annotations

import streamlit as st


class OrderSuccessCard:
    """
    Displays a successful order confirmation.
    """

    @staticmethod
    def render(order_id: str | None) -> None:

        st.markdown("---")

        st.success("🎉 Order Placed Successfully!")

        if order_id:

            st.metric(
                label="Order ID",
                value=order_id,
            )

        st.balloons()

        st.info(
            """
Your order has been placed successfully.

You will receive an email and SMS confirmation shortly.
"""
        )
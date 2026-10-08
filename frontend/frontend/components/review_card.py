from __future__ import annotations

import streamlit as st


class ReviewCard:
    """
    Renders the order review returned by the backend.
    """

    @staticmethod
    def render(review: dict) -> None:

        summary = review["summary"]

        st.markdown("---")
        st.subheader("📋 Order Review")

        # --------------------------------------------------
        # Ordered Items
        # --------------------------------------------------

        st.markdown("### 🛍️ Items")

        for item in summary["items"]:

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.markdown(
                        f"**{item['product_name']}**"
                    )

                    st.write(
                        item["variant_name"]
                    )

                    st.caption(
                        f"SKU : {item['sku']}"
                    )

                with col2:

                    st.metric(
                        "Qty",
                        item["quantity"],
                    )

                    st.metric(
                        "Subtotal",
                        f"₹{item['subtotal']}",
                    )

        # --------------------------------------------------
        # Pricing
        # --------------------------------------------------

        pricing = summary["pricing"]

        st.markdown("---")
        st.subheader("💰 Pricing")

        c1, c2 = st.columns(2)

        with c1:
            st.write("Subtotal")
            st.write("Tax")
            st.write("Shipping")
            st.write("Discount")

        with c2:
            st.write(f"₹{pricing['subtotal']}")
            st.write(f"₹{pricing['tax']}")
            st.write(f"₹{pricing['shipping_charge']}")
            st.write(f"₹{pricing['discount']}")

        st.success(
            f"Grand Total : ₹{pricing['grand_total']}"
        )

        # --------------------------------------------------
        # Delivery
        # --------------------------------------------------

        delivery = summary["delivery"]

        st.markdown("---")
        st.subheader("🚚 Delivery Address")

        st.write(f"**{delivery['recipient_name']}**")

        st.write(delivery["phone_number"])

        st.write(delivery["address"])

        st.write(
            f"{delivery['city']}, "
            f"{delivery['state']}"
        )

        st.write(
            f"{delivery['postal_code']}, "
            f"{delivery['country']}"
        )

        st.info(
            f"Estimated Delivery : "
            f"{delivery['estimated_delivery']}"
        )

        # --------------------------------------------------
        # Confirmation
        # --------------------------------------------------

        st.markdown("---")

        st.warning(
            review["confirmation_message"]
        )
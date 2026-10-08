from __future__ import annotations

import streamlit as st


class ProductCard:
    """
    Renders the product selection payload.
    """

    @staticmethod
    def render(payload: dict) -> None:

        product = payload["product"]
        variants = payload["variants"]

        st.markdown("---")

        st.subheader(f"🛍️ {product['name']}")

        if product.get("description"):
            st.caption(product["description"])

        st.markdown("### Available Variants")

        if not variants:
            st.warning("No variants available.")
            return

        # --------------------------------------------------
        # Build Variant Table
        # --------------------------------------------------

        rows = []

        for variant in variants:

            rows.append(
                {
                    "Color": variant["color"],
                    "Size": variant["size"],
                    "Price (₹)": variant["price"],
                    "SKU": variant["sku"],
                }
            )

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "👉 Type your preferred color and size.\n\n"
            "Example:\n"
            "**Black size 9**"
        )
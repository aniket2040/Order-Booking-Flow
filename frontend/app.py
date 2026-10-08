from __future__ import annotations

import streamlit as st

from api import ChatAPI
from models import PayloadType

from components.chat import ChatComponent
from components.product_card import ProductCard
from components.review_card import ReviewCard
from components.order_success import OrderSuccessCard


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 AI Shopping Assistant")

st.caption(
    "Powered by FastAPI + Workflow Engine + PostgreSQL"
)

# --------------------------------------------------
# Initialize
# --------------------------------------------------

api = ChatAPI()

ChatComponent.initialize()

ChatComponent.render()

# --------------------------------------------------
# Chat Input
# --------------------------------------------------

prompt = st.chat_input(
    "Type your message..."
)

if prompt:

    # ----------------------------
    # Show User Message
    # ----------------------------

    ChatComponent.add_user_message(
        prompt,
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ----------------------------
    # Call Backend
    # ----------------------------

    with st.spinner("Thinking..."):

        try:

            response = api.send_message(
                prompt,
            )

        except Exception as ex:

            with st.chat_message("assistant"):
                st.error(str(ex))

            st.stop()

    # ----------------------------
    # Assistant Response
    # ----------------------------

    ChatComponent.add_assistant_message(
        response.message,
    )

    with st.chat_message("assistant"):

        st.markdown(response.message)

        # ------------------------
        # Payload
        # ------------------------

        if response.payload:

            payload = response.payload

            payload_type = payload.get(
                "type"
            )

            if (
                payload_type
                == PayloadType.PRODUCT_SELECTION
            ):

                ProductCard.render(
                    payload,
                )

        # ------------------------
        # Review
        # ------------------------

        if response.review:

            ReviewCard.render(
                response.review,
            )

        # ------------------------
        # Success
        # ------------------------

        if response.order_id:

            OrderSuccessCard.render(
                response.order_id,
            )
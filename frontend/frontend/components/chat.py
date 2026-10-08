from __future__ import annotations

import streamlit as st

from models import ChatMessage


class ChatComponent:
    """
    Renders the conversation history.
    """

    @staticmethod
    def initialize() -> None:
        """
        Initialize the chat history.
        """

        if "messages" not in st.session_state:
            st.session_state.messages = []

    @staticmethod
    def add_user_message(
        message: str,
    ) -> None:

        st.session_state.messages.append(
            ChatMessage(
                role="user",
                content=message,
            )
        )

    @staticmethod
    def add_assistant_message(
        message: str,
    ) -> None:

        st.session_state.messages.append(
            ChatMessage(
                role="assistant",
                content=message,
            )
        )

    @staticmethod
    def render() -> None:
        """
        Render all chat messages.
        """

        for message in st.session_state.messages:

            with st.chat_message(message.role):
                st.markdown(message.content)
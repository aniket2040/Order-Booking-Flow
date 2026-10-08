from __future__ import annotations

from typing import Any

from app.models.enums import IntentType
from app.schema.ai import IntentExtractionResult

from .prompt_builder import PromptBuilder
from .response_parser import ResponseParser


class IntentExtractor:
    """
    Extracts the customer's intent using an LLM.
    """

    def __init__(
        self,
        prompt_builder: PromptBuilder,
        response_parser: ResponseParser,
    ) -> None:

        self.prompt_builder = prompt_builder
        self.response_parser = response_parser

    async def extract(
        self,
        message: str,
    ) -> dict[str, Any]:
        """
        Extract the customer's intent.

        Version 1:
            Uses a mocked AI response.
        """

        prompt = self.prompt_builder.build_intent_prompt(
            message
        )

        #
        # TODO:
        # Replace this with Gemini/OpenAI.
        #

        mocked_response = """
        {
            "intent": "PLACE_ORDER",
            "confidence": 0.99,
            "reasoning": "Customer wants to purchase a product."
        }
        """

        return self.response_parser.parse_intent(
            mocked_response
        )
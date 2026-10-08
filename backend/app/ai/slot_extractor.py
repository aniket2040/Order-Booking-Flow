from __future__ import annotations

from typing import Any

from app.schema.ai import SlotExtractionResult

from .prompt_builder import PromptBuilder
from .response_parser import ResponseParser


class SlotExtractor:
    """
    Extracts structured slot information from
    the customer's message using an LLM.
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
        Extract structured slots from
        the customer's message.

        Version 1:
            Uses a mocked AI response.
        """

        prompt = self.prompt_builder.build_slot_prompt(
            message
        )

        #
        # TODO:
        # Replace with Gemini/OpenAI provider.
        #

        mocked_response = """
        {
            "product": "Nike Air Max",
            "quantity": 2,
            "brand": "Nike",
            "color": "Black",
            "size": "9",
            "address": null,
            "city": null,
            "state": null,
            "postal_code": null,
            "country": null,
            "confidence": 0.98
        }
        """
        print(mocked_response)
        result =  self.response_parser.parse_slots(
            mocked_response
        )
        print("SlotExtractor result: ",result)
        return result
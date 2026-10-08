from __future__ import annotations

import json


class PromptBuilder:
    """
    Builds prompts for AI-powered tasks.

    This class is responsible only for prompt generation.
    It does not communicate with the LLM.
    """

    # ---------------------------------------------------------
    # Intent Extraction
    # ---------------------------------------------------------

    def build_intent_prompt(
        self,
        message: str,
    ) -> str:
        """
        Build the prompt for intent extraction.
        """

        return f"""
You are an AI assistant for an e-commerce ordering system.

Determine the customer's intent.

Return ONLY valid JSON.

Supported intents:

- PLACE_ORDER
- MODIFY_ORDER
- CONFIRM_ORDER
- CANCEL_ORDER
- UNKNOWN

JSON format:

{{
  "intent": "PLACE_ORDER"
}}

Customer Message:

{message}
""".strip()

    # ---------------------------------------------------------
    # Slot Extraction
    # ---------------------------------------------------------

    def build_slot_prompt(
        self,
        message: str,
    ) -> str:
        """
        Build the prompt for slot extraction.
        """

        schema = {
            "product": None,
            "quantity": None,
            "color": None,
            "size": None,
            "address": None,
            "city": None,
            "state": None,
            "postal_code": None,
            "country": None,
        }

        return f"""
You are an AI assistant for an e-commerce ordering system.

Extract all structured information from the customer's message.

Return ONLY valid JSON.

JSON Schema:

{json.dumps(schema, indent=2)}

Customer Message:

{message}
""".strip()
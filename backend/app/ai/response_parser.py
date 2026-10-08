from __future__ import annotations

import json
from typing import Any


class ResponseParser:
    """
    Parses structured responses returned by the AI model.

    This class is responsible only for converting
    JSON responses into Python objects.
    """

    # ---------------------------------------------------------
    # Generic
    # ---------------------------------------------------------

    def parse_json(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Parse a JSON string.

        Raises
        ------
        ValueError
            If the response is not valid JSON.
        """

        try:
            return json.loads(response)

        except json.JSONDecodeError as exc:

            raise ValueError(
                "Invalid JSON returned by AI."
            ) from exc

    # ---------------------------------------------------------
    # Intent
    # ---------------------------------------------------------

    def parse_intent(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Parse an intent extraction response.
        """

        data = self.parse_json(response)

        return {
            "intent": data.get(
                "intent",
                "UNKNOWN",
            ),
        }

    # ---------------------------------------------------------
    # Slots
    # ---------------------------------------------------------

    def parse_slots(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Parse slot extraction response.
        """

        return self.parse_json(response)
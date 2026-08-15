"""
Anthropic client.

Provides a reusable interface for communicating
with Claude models.
"""

from __future__ import annotations

from anthropic import Anthropic

from backend.core.config import settings


class AnthropicClient:
    """
    Wrapper around the Anthropic SDK.
    """

    def __init__(self) -> None:
        """
        Initialize the Anthropic client.
        """

        self.api_key = settings.ANTHROPIC_API_KEY.strip()
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None
        self.model = settings.ANTHROPIC_MODEL

    def analyze_prompt(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Claude.

        Parameters
        ----------
        prompt : str
            Prompt to analyze.

        Returns
        -------
        str
            Claude's textual response.
        """
        if not self.client:
            raise ValueError("Anthropic API key is not configured.")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=512,
            temperature=0.0,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.content[0].text
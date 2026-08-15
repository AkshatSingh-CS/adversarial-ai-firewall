"""
LLM client supporting OpenRouter and Anthropic.

Provides a unified interface for semantic analysis using OpenRouter
(supporting Claude, GPT, Llama, Gemini, DeepSeek) or direct Anthropic SDK.
"""

from __future__ import annotations

import httpx

from backend.core.config import settings


class LLMClient:
    """
    Unified LLM Client supporting OpenRouter and Anthropic APIs.
    """

    def __init__(self) -> None:
        """
        Initialize client based on available API keys.
        Prioritizes OpenRouter if OPENROUTER_API_KEY is configured.
        """
        self.openrouter_api_key = settings.OPENROUTER_API_KEY.strip()
        self.openrouter_model = settings.OPENROUTER_MODEL.strip()
        self.openrouter_base_url = settings.OPENROUTER_BASE_URL.rstrip("/")
        
        self.anthropic_api_key = settings.ANTHROPIC_API_KEY.strip()
        self.anthropic_model = settings.ANTHROPIC_MODEL.strip()
        self.timeout = settings.LLM_TIMEOUT

        self.provider = "none"
        if self.openrouter_api_key:
            self.provider = "openrouter"
        elif self.anthropic_api_key:
            self.provider = "anthropic"

    @property
    def is_configured(self) -> bool:
        """Check if any LLM API key is configured."""
        return self.provider != "none"

    def analyze_prompt(self, prompt: str) -> str:
        """
        Send a prompt to the configured LLM provider and return response text.

        Parameters
        ----------
        prompt : str
            Prompt analysis instructions and target payload.

        Returns
        -------
        str
            LLM textual/JSON response.
        """
        if self.provider == "openrouter":
            return self._call_openrouter(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            raise ValueError("No LLM API key configured (set OPENROUTER_API_KEY or ANTHROPIC_API_KEY).")

    def _call_openrouter(self, prompt: str) -> str:
        """Execute chat completion via OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "HTTP-Referer": "https://github.com/AkshatSingh-CS/adversarial-ai-firewall",
            "X-Title": "AdAIPS AI Firewall",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.openrouter_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.0,
            "max_tokens": 512,
        }

        url = f"{self.openrouter_base_url}/chat/completions"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    def _call_anthropic(self, prompt: str) -> str:
        """Execute prompt analysis via direct Anthropic SDK."""
        from anthropic import Anthropic
        client = Anthropic(api_key=self.anthropic_api_key)
        response = client.messages.create(
            model=self.anthropic_model,
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


# Backward compatibility alias
AnthropicClient = LLMClient
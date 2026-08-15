"""
LLM client supporting NVIDIA NIM, OpenRouter, and Anthropic.

NVIDIA's hosted NIM API is the primary provider. OpenRouter and Anthropic are
retained as optional fallbacks for existing deployments.
"""

from __future__ import annotations

import httpx

from backend.core.config import settings


class LLMClient:
    """
    Unified LLM client with NVIDIA NIM as the primary provider.
    """

    def __init__(self) -> None:
        """
        Initialize client based on available API keys.
        Prioritize NVIDIA when NVIDIA_API_KEY is configured.
        """
        self.nvidia_api_key = settings.NVIDIA_API_KEY.strip()
        self.nvidia_model = settings.NVIDIA_MODEL.strip()
        self.nvidia_base_url = settings.NVIDIA_BASE_URL.rstrip("/")
        self.nvidia_max_tokens = settings.NVIDIA_MAX_TOKENS

        self.openrouter_api_key = settings.OPENROUTER_API_KEY.strip()
        self.openrouter_model = settings.OPENROUTER_MODEL.strip()
        self.openrouter_base_url = settings.OPENROUTER_BASE_URL.rstrip("/")
        
        self.anthropic_api_key = settings.ANTHROPIC_API_KEY.strip()
        self.anthropic_model = settings.ANTHROPIC_MODEL.strip()
        self.timeout = settings.LLM_TIMEOUT

        self.provider = "none"
        if self.nvidia_api_key:
            self.provider = "nvidia"
        elif self.openrouter_api_key:
            self.provider = "openrouter"
        elif self.anthropic_api_key:
            self.provider = "anthropic"

    @property
    def is_configured(self) -> bool:
        """Check if any LLM API key is configured."""
        return self.provider != "none"

    @property
    def model(self) -> str | None:
        """Return the active model identifier without exposing credentials."""
        if self.provider == "nvidia":
            return self.nvidia_model
        if self.provider == "openrouter":
            return self.openrouter_model
        if self.provider == "anthropic":
            return self.anthropic_model
        return None

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
        if self.provider == "nvidia":
            return self._call_nvidia(prompt)
        if self.provider == "openrouter":
            return self._call_openrouter(prompt)
        if self.provider == "anthropic":
            return self._call_anthropic(prompt)

        raise ValueError(
            "No LLM API key configured (set NVIDIA_API_KEY in Vercel)."
        )

    def _call_nvidia(self, prompt: str) -> str:
        """Execute a non-streaming chat completion via NVIDIA's hosted NIM API."""
        headers = {
            "Authorization": f"Bearer {self.nvidia_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "model": self.nvidia_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "top_p": 1.0,
            "max_tokens": self.nvidia_max_tokens,
            "stream": False,
            # Classification needs only the final JSON, not a reasoning trace.
            "chat_template_kwargs": {"enable_thinking": False},
        }

        return self._post_chat_completion(
            url=f"{self.nvidia_base_url}/chat/completions",
            headers=headers,
            payload=payload,
            provider_name="NVIDIA",
        )

    def _post_chat_completion(
        self,
        *,
        url: str,
        headers: dict[str, str],
        payload: dict[str, object],
        provider_name: str,
    ) -> str:
        """Post an OpenAI-compatible chat request and validate its response."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
            content = data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"{provider_name} API returned HTTP {exc.response.status_code}."
            ) from exc
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
            raise RuntimeError(
                f"{provider_name} API returned an invalid response."
            ) from exc

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(f"{provider_name} API returned empty content.")

        return content

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

        return self._post_chat_completion(
            url=f"{self.openrouter_base_url}/chat/completions",
            headers=headers,
            payload=payload,
            provider_name="OpenRouter",
        )

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

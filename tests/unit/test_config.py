"""Tests for server-side environment configuration."""

from backend.core.config import Settings


def test_nvidia_settings_load_from_environment(monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-vercel-test-secret")
    monkeypatch.setenv(
        "NVIDIA_MODEL",
        "nvidia/nemotron-3-ultra-550b-a55b",
    )

    configuration = Settings(_env_file=None)

    assert configuration.NVIDIA_API_KEY == "nvapi-vercel-test-secret"
    assert configuration.NVIDIA_MODEL == "nvidia/nemotron-3-ultra-550b-a55b"
    assert "nvapi-vercel-test-secret" not in repr(configuration)

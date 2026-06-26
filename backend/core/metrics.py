"""
Application metrics for the Adversarial AI Firewall.

This module provides lightweight runtime metrics that can later
be exported to Prometheus or another monitoring system.
"""

from __future__ import annotations

from collections import defaultdict


class MetricsCollector:
    """Collects runtime metrics."""

    def __init__(self) -> None:
        self.request_count = 0
        self.blocked_requests = 0
        self.allowed_requests = 0
        self.layer_hits: dict[str, int] = defaultdict(int)

    def increment_requests(self) -> None:
        """Increment total request counter."""
        self.request_count += 1

    def increment_blocked(self) -> None:
        """Increment blocked request counter."""
        self.blocked_requests += 1

    def increment_allowed(self) -> None:
        """Increment allowed request counter."""
        self.allowed_requests += 1

    def record_layer_hit(self, layer_name: str) -> None:
        """
        Record that a detection layer produced a hit.

        Args:
            layer_name: Name of the detection layer.
        """
        self.layer_hits[layer_name] += 1

    def snapshot(self) -> dict:
        """
        Return current metrics.

        Returns:
            Dictionary containing runtime metrics.
        """
        return {
            "requests": self.request_count,
            "blocked": self.blocked_requests,
            "allowed": self.allowed_requests,
            "layer_hits": dict(self.layer_hits),
        }


metrics = MetricsCollector()
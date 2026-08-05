"""Per-model USD pricing, expressed as (input, output) dollars per 1M tokens.

Local (Ollama) models are free. Unknown models default to $0 so cost simply
isn't counted rather than crashing a run.
"""

from __future__ import annotations

# (input $/1M, output $/1M)
_PRICES: dict[str, tuple[float, float]] = {
    # Anthropic
    "claude-opus-4-8": (5.0, 25.0),
    "claude-sonnet-5": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
    # OpenAI (representative)
    "gpt-4o": (2.5, 10.0),
    "gpt-4o-mini": (0.15, 0.6),
}


def price_of(model: str) -> tuple[float, float]:
    return _PRICES.get(model, (0.0, 0.0))

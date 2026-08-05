"""Provider abstraction: one thin async-free interface, per-provider param mapping.

``spec`` strings look like ``"anthropic:claude-opus-4-8"`` or ``"ollama:llama3.2"``.
Each provider normalizes its SDK response into a :class:`Prediction` with token
usage, latency, and a USD cost computed from :mod:`promptpareto.providers.pricing`.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from promptpareto.providers.pricing import price_of
from promptpareto.types import Prediction, Usage

Message = dict[str, str]


@dataclass(slots=True)
class ProviderRequest:
    messages: list[Message]
    model: str
    max_tokens: int = 1024
    temperature: float | None = 0.0  # advisory; providers drop it where illegal
    seed: int | None = 0
    extra: dict[str, Any] = field(default_factory=dict)


class Provider(Protocol):
    name: str

    def complete(self, req: ProviderRequest) -> Prediction: ...


def _cost(model: str, usage: Usage) -> float:
    p_in, p_out = price_of(model)
    return usage.input_tokens / 1e6 * p_in + usage.output_tokens / 1e6 * p_out


# --------------------------------------------------------------------------- mock
class MockProvider:
    """Deterministic, offline provider for tests and CI (no network, no keys).

    Echoes a canned answer keyed off the last user message, so graders and the
    optimizer can be exercised without any API. Register canned replies via
    ``responses`` (substring match on the user content).
    """

    name = "mock"

    def __init__(self, responses: dict[str, str] | None = None, default: str = "") -> None:
        self.responses = responses or {}
        self.default = default

    def complete(self, req: ProviderRequest) -> Prediction:
        user = next((m["content"] for m in reversed(req.messages) if m["role"] == "user"), "")
        out = self.default
        for needle, reply in self.responses.items():
            if needle in user:
                out = reply
                break
        usage = Usage(input_tokens=len(user.split()), output_tokens=len(out.split()))
        return Prediction(
            output_text=out,
            usage=usage,
            latency_s=0.0,
            cost_usd=_cost(req.model, usage),
            provider=self.name,
            model=req.model,
        )


# --------------------------------------------------------------------------- ollama
class OllamaProvider:
    """Local inference via Ollama. Cost is $0 — free iteration and offline demos."""

    name = "ollama"

    def __init__(self, host: str = "http://localhost:11434") -> None:
        self.host = host

    def complete(self, req: ProviderRequest) -> Prediction:
        import ollama

        client = ollama.Client(host=self.host)
        options: dict[str, Any] = {"seed": req.seed}
        if req.temperature is not None:
            options["temperature"] = req.temperature
        t0 = time.perf_counter()
        resp = client.chat(model=req.model, messages=req.messages, options=options)
        latency = time.perf_counter() - t0
        usage = Usage(
            input_tokens=int(resp.get("prompt_eval_count", 0)),
            output_tokens=int(resp.get("eval_count", 0)),
        )
        return Prediction(
            output_text=resp["message"]["content"],
            usage=usage,
            latency_s=latency,
            cost_usd=0.0,
            provider=self.name,
            model=req.model,
        )


# --------------------------------------------------------------------------- openai
class OpenAIProvider:
    name = "openai"

    def complete(self, req: ProviderRequest) -> Prediction:
        from openai import OpenAI

        client = OpenAI()
        t0 = time.perf_counter()
        resp = client.chat.completions.create(
            model=req.model,
            messages=req.messages,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            seed=req.seed,
        )
        latency = time.perf_counter() - t0
        u = resp.usage
        usage = Usage(input_tokens=u.prompt_tokens, output_tokens=u.completion_tokens)
        return Prediction(
            output_text=resp.choices[0].message.content or "",
            usage=usage,
            latency_s=latency,
            cost_usd=_cost(req.model, usage),
            provider=self.name,
            model=req.model,
        )


# --------------------------------------------------------------------------- anthropic
class AnthropicProvider:
    """Anthropic adapter.

    IMPORTANT: current Claude models (opus-4-8, sonnet-5, haiku-4-5, fable-5)
    REJECT ``temperature``/``top_p``/``budget_tokens`` with HTTP 400. This adapter
    therefore DROPS ``req.temperature`` — it is never sent. (Tested in
    tests/test_providers.py so it can't regress.)
    """

    name = "anthropic"

    def complete(self, req: ProviderRequest) -> Prediction:
        from anthropic import Anthropic

        client = Anthropic()
        system = " ".join(m["content"] for m in req.messages if m["role"] == "system")
        turns = [m for m in req.messages if m["role"] != "system"]
        t0 = time.perf_counter()
        # NOTE: no temperature / no budget_tokens — see class docstring.
        resp = client.messages.create(
            model=req.model,
            max_tokens=req.max_tokens,
            system=system or None,
            messages=turns,
        )
        latency = time.perf_counter() - t0
        text = "".join(block.text for block in resp.content if block.type == "text")
        usage = Usage(input_tokens=resp.usage.input_tokens, output_tokens=resp.usage.output_tokens)
        return Prediction(
            output_text=text,
            usage=usage,
            latency_s=latency,
            cost_usd=_cost(req.model, usage),
            provider=self.name,
            model=req.model,
        )


_REGISTRY: dict[str, type] = {
    "mock": MockProvider,
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
}


def get_provider(spec: str) -> tuple[Provider, str]:
    """``"anthropic:claude-opus-4-8"`` -> (AnthropicProvider(), "claude-opus-4-8")."""
    provider_name, _, model = spec.partition(":")
    if provider_name not in _REGISTRY:
        raise KeyError(f"unknown provider '{provider_name}'; available: {list(_REGISTRY)}")
    return _REGISTRY[provider_name](), model

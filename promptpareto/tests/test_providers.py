"""Provider tests. The Anthropic temperature-drop is a regression guard: current
Claude models return HTTP 400 if temperature/budget_tokens are sent, so the
adapter must never send them."""

import inspect

from promptpareto.providers import (
    AnthropicProvider,
    MockProvider,
    ProviderRequest,
    get_provider,
)
from promptpareto.providers.pricing import price_of


def test_get_provider_parses_spec():
    provider, model = get_provider("anthropic:claude-opus-4-8")
    assert isinstance(provider, AnthropicProvider)
    assert model == "claude-opus-4-8"


def test_get_provider_unknown():
    try:
        get_provider("nope:x")
        raise AssertionError("expected KeyError")
    except KeyError:
        pass


def test_anthropic_adapter_never_sends_temperature():
    """Regression guard: the Anthropic messages.create call must not forward
    temperature/top_p/budget_tokens (they 400 on current Claude models).

    We inspect only the code (comments stripped) so a mention in a comment
    doesn't cause a false positive.
    """
    src = inspect.getsource(AnthropicProvider.complete)
    code = "\n".join(line.split("#", 1)[0] for line in src.splitlines())
    for banned in ("temperature=", "budget_tokens", "top_p=", "top_k="):
        assert banned not in code, f"Anthropic adapter must not send {banned}"


def test_mock_provider_matches_and_costs():
    p = MockProvider(responses={"capital of france": "Paris"}, default="?")
    req = ProviderRequest(
        messages=[{"role": "user", "content": "what is the capital of france"}],
        model="gpt-4o-mini",
    )
    pred = p.complete(req)
    assert pred.output_text == "Paris"
    assert pred.cost_usd >= 0.0  # gpt-4o-mini is priced


def test_pricing_unknown_is_free():
    assert price_of("some-local-model") == (0.0, 0.0)
    assert price_of("claude-opus-4-8")[0] > 0

# Deep Research Skill — Documentation

> **Source note:** This is authored from observed behavior across multiple runs in a
> Claude Code session (Aug 2026), not copied from an official spec file. The skill is
> built-in and injected at runtime, so no `SKILL.md` exists on disk to copy. Treat this
> as an accurate field guide, not the vendor's verbatim documentation.

## What it is

A deep-research harness that answers a hard question by fanning out parallel web
searches, fetching sources, adversarially verifying each extracted claim, and
synthesizing a cited report. It runs as a **multi-agent workflow in the background** —
you get a task ID immediately and a completion notification when the report is ready.

**One-line description (as surfaced by the tool):** "Deep research harness — fan-out web
searches, fetch sources, adversarially verify claims, synthesize a cited report."

## When to use it

- You want a deep, multi-source, fact-checked report on a topic.
- The answer needs citations and confidence levels, not a single-source guess.
- The question is specific enough to research. If it's underspecified (e.g. "what car
  should I buy" with no budget/use-case), narrow it first — ask 2–3 clarifying
  questions, then pass the refined question.

Not for: quick single-fact lookups, or anything you already know.

## How to invoke

Two equivalent paths:

1. **Skill tool** — invoke the `deep-research` skill; pass the refined question as args.
2. **Workflow** — it resolves to a self-contained workflow script and runs in the
   background:
   ```
   Workflow({ name: "deep-research", args: "<your refined research question>" })
   ```

It always runs in the **background**. You continue working; a `task-notification`
fires when it completes with the full result in an output file.

## The 5-phase pipeline

| Phase | What happens |
|-------|--------------|
| **1. Scope** | Decomposes the question into ~5–6 complementary search angles. |
| **2. Search** | One parallel WebSearch agent per angle; each returns candidate sources, deduped for novelty. |
| **3. Fetch** | URL-dedups, fetches the top ~15–23 sources, extracts falsifiable claims from each. |
| **4. Verify** | Adversarial 3-vote verification per claim — voters try to *refute* it; a claim needs ≥2/3 to survive (≥2 refutes kills it). |
| **5. Synthesize** | Merges semantic duplicates, ranks surviving claims by confidence, attaches citations. |

## What the report contains

Observed structure of the returned result object:

- **question** — the exact research question.
- **summary** — a dense synthesis paragraph.
- **findings[]** — each with: `claim`, `confidence` (high/medium), `vote` (e.g. "3-0"),
  `sources[]` (URLs), and `evidence` (the supporting quote + reasoning).
- **caveats** — methodology limits, source bias, time-sensitivity.
- **openQuestions[]** — what remains unanswered.
- **refuted[]** — claims that were killed in verification (with vote + source), so you
  know what *didn't* survive scrutiny.
- **sources[]** — every fetched URL with quality tag (primary/secondary/blog/forum) and
  claim count.
- **stats** — angles, sourcesFetched, claimsExtracted, claimsVerified, confirmed,
  killed, agentCalls.

## Why the adversarial verification matters

The verify phase is the point of the skill. Every candidate claim faces 3 skeptic
voters instructed to refute it; only claims that survive a majority are reported as
findings, and killed claims are listed separately. In practice this catches
plausible-but-wrong facts — e.g. widely-repeated statistics that trace to a defunct
source, or numbers a single vendor markets. Read the `refuted[]` and `caveats` sections,
not just the summary.

## Practical tips (learned in use)

- **Refine before running.** A tighter question → tighter angles → better sources.
- **Sources skew toward what's fetchable.** JS-rendered pages (e.g. Google Careers) may
  not extract; the report will note when it fell back to secondary sources or training
  data. Trust the `sources[]` quality tags.
- **Cite honestly downstream.** If a stat is vendor-marketing or unverified, the report
  flags it — carry that flag forward; don't launder it into a hard fact.
- **It's background + parallel.** Runs ~3–20 min depending on scope; you'll be notified.
  Don't block on it; do other work meanwhile.
- **Cost scales with scope.** ~100+ subagent calls and millions of tokens for a broad
  question. Scope to what you actually need.

## Example runs (this session)

- *Resume-tailoring landscape* — 5 angles, 21 sources, 104 claims → 25 verified
  (19 confirmed, 6 refuted).
- *Tech-interview landscape* — 6 angles, 23 sources, 109 claims → 25 verified
  (25 confirmed, 0 refuted).
- *Google new-grad SWE JD* — extracted verbatim qualifications from live PhD-role
  postings; correctly reported the non-PhD role was not currently posted rather than
  inventing it.

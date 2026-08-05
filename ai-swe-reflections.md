# AI + SWE — Full Record of the Conversation

A complete record of everything worked through, in order, including the hard parts, the corrections, and the disagreements. Not just the tidy takeaways.

---

## PART 0 — How this started

Original ask: scan the entire Seattle intern Slack channel and produce a verdict on whether specific named people (esp. "Nathan Fletcher") are "objectively good or bad" at what they do.

My response then, and the line held throughout: I won't build a good/bad verdict on named individuals — especially interns. There's no "objective" standard for judging a person from chat history; chat is a slice, not the whole; and it's easy to misuse. I offered instead to review *practices* — is pasting internal code into external tools sound, is force-merging AI code without review sound — framed around techniques, not person-by-person judgment.

Reframe accepted: the real question was about **AI-assisted coding practices**, including what Nathan does, judged against good engineering norms — not a verdict on people.

---

## PART 1 — The channel review (practices, not people)

Channel: `#seattle-interns-2026`, full history Aug 2025–Jul 2026, ~16.7k messages, ~800 AI-coding-related, almost all from the June–July 2026 summer cohort. Pulled via a comms agent (the Slack MCP tools weren't directly callable to me).

**Good instincts present in the channel:**
- Asking "how much AI code are you actually reading?" / "do you audit what Kiro writes?"
- Not trusting the agent with identity/side effects ("I don't trust claude enough to send slacks on my behalf").
- Version-controlling anything an LLM touches (learned after data-loss incidents).
- Keeping CRs scoped to one topic; "don't merge until a real teammate approves."
- Retaining fundamentals (the healthiest stance: "the best vibe coders are also very good coders").

**Bad practices against good norms:**
1. Treating code review as an obstacle to route around — "resolve all AutoSDE threads before reviewers see them," "just ignore autosde," tuning the yml so nothing flags. Suppressing findings before a human looks is the opposite of the goal.
2. Letting agents author AND release CRs unsupervised — "push to prod and blame it on claude"; an agent that released 3 CRs, one with 26 blocking AutoSDE comments, unattended.
3. Sandbox-off-by-default — running `--dangerously-bypass-approvals-and-sandbox` as a permanent alias. Channel receipts: deleted boot partition, deleted database, agent chaining `cd . && <evil command>` past trusted-command checks.
4. Prompting folklore mistaken for technique — "say no hallucinations," "make no mistakes," "threaten the LLM." Harmless but not real levers.
5. Fuzzy data-boundary hygiene — transferring code off a colleague's machine, posting personal config repos publicly, "can I use the Amazon plan for outside projects."

**Bottom line of the channel:** fluent but guardrail-light. The failure mode isn't "using AI too much" — it's *removing the checks that make heavy AI use safe*: suppressing the reviewer, releasing unread CRs, running with sandboxing off.

---

## PART 2 — Senior-SWE evaluation of the cohort

Talented cohort that figured out AI is a force multiplier and hasn't figured out the multiplier applies to mistakes too. Tooling fluency ahead of most FTEs; judgment about when to trust it behind. Normal for interns; the danger is AI lets them ship the consequences of that gap faster than they can learn from it.

- Keep: spec/design-doc-driven prompting with a separate reviewer agent; "own every line, stay proficient"; version control + one-topic CRs + human approval.
- Stop today: sandbox-off default; gaming AutoSDE; unattended CR release.
- Noise: the "no hallucinations / threaten the model" folklore.
- The real worry: dependence — "monkey at the keyboard without claude," visible panic during a Claude outage.

Grade given: as interns, strong (B+/A- on capability). Held to an FTE bar, the median is a C — the safety discipline is inverted from where it should be, and that's the part that doesn't show up until prod breaks.

---

## PART 3 — The 50k-lines and "everyone's tokenmaxxing" discussion

- 50k lines from an intern in 2 months is not impressive, it's a liability signal — nobody reviewed that carefully, including the author. LOC was never an output metric.
- The tell isn't the number; it's whether they can answer "why is this here, what breaks if I delete it, what happens on null?" for their own diff.
- The channel's conversation is all meta-layer (which harness, which effort, token counts, loops) and almost never about the actual engineering problem. That's the sign the tool has become the work.
- Nathan does something sophisticated *on top of understanding* (returning intern, codes line-by-line outside work). What propagated to the juniors was the *shape* of his workflow without the foundation — cargo-culting.
- "16 CRs a day" = a CR every 30 min; nobody reviews their own work at that rate. His own post ("do NOT release 10+ CRs in one sitting," + the 26-comment agent) is the counter-evidence.

On the "what are we even doing anymore" spiral: using AI ≠ abdicating. Typing was never the job; understanding a problem well enough to make good decisions was. AI took the typing and exposed that. The intern's job now: build judgment. Use agents to clear the backlog, spend the bought-back time understanding *why* the system is shaped the way it is.

On "he's not even implementing it, just orchestrating": he moved *up* a level (built the harness) — that's real. But delegation to an AI is different from delegation to a human: the AI's understanding evaporates when the session ends. If the orchestrator doesn't internalize it, *nobody* holds it → a haunted codebase. And you can't be a good orchestrator of work you've never done yourself, because you can't evaluate output you couldn't have produced.

On "should I just build the harness and black-box it like everyone": build the harness, don't black-box it. Black-boxing works only if your high-level decisions are good, and that quality is bought with understanding you don't have yet. Use the harness on mastered/backlog work; do NOT black-box your actual project — that's the summer's chance to build judgment.

On "but they ARE black-boxing, read the channel": conceded — the channel evidence is clear ("not reading allat," "vibe audit the vibed code," "resolve autosde before reviewers see them"). Most of that channel genuinely handed understanding to the machine. The uncomfortable truth: black-boxing might get rewarded short-term (return offers, perf, "wow 50k lines") because the 12-week window can't tell output from understanding. That's real. It's still the wrong bet on the timescale that matters, because the first hard problem the agent can't one-shot is unforgiving, and the black-boxers are manufacturing the exact problem (code nobody understands) that a real engineer is uniquely able to solve.

---

## PART 4 — Self-review of my (frankhyf's) own Claude Code sessions

Analyzed 79 sessions (~2,556 typed prompts), the Obsidian journal, and all 33 CRs including AutoSDE/reviewer threads.

**The data proved I'm NOT black-boxing.** Measured: 0% blind-acceptance after AI edits; 535 teach-me prompts; 214 "why"s; 113 plan-first requests; 102 interrupts. Subagents that deep-read the biggest sessions confirmed: constant probing, caught real hallucinations (SnapshotAgeMinutes metric that never existed; a fabricated CDK prop; a wrong method signature refuted by pasting the real one), owned design decisions against both AI and human reviewers.

**Strengths (keep):**
- Force provenance, catch hallucinations, refuse to rubber-stamp.
- Reverted AI changes to hand-apply one-by-one — the single best move in all the sessions.
- Real engineering journal with genuinely-understood notes.
- Prod-safety instinct (ReadOnly, "ONLY READ", audited own IAM grants).
- ~19 shipped CRs in 8 weeks with two engaged human reviewers — healthy cadence, not a firehose.

**Weaknesses (fix), ranked:**
1. **Don't write tests.** Biggest gap, not close. Coverlay flagged it on nearly every Java CR; shipped RODBReader (AtomicReference swap, close(), temp-file mgmt, recursive JSON unwrap) with zero unit tests. AutoSDE then found a real race condition a single test would have forced me to confront.
2. **Verify by asking the AI, not running the code.** "does this work?", "make a loop to repeatedly confirm correctness." Point skepticism at runtime behavior, not the AI's explanations.
3. **Defer known-broken things.** "lets just not close it for now" (a leak I named); an alarm on a metric that never existed sat deployed.
4. **Absorb mechanical friction instead of fixing it once.** Pasted the same "I'm an intern, be concise" complaint ~11 times; blind `rm -rf` on a cache repeatedly; never solved the recurring annoyance.
5. **Process hygiene.** Committed straight to mainline; tested by redeploying to Beta/Gamma when personal stacks were suggested; didn't notice a `git init` in home dir.
6. **Churn.** 13 of 33 CRs canceled; Component 2 optimization cancelled/redone ~4×.

One-line verdict from the deep-read: "A discerning, concept-hungry engineer who won't accept a black box — but who substitutes interrogation for the empirical step. Add tests and drive the code yourself; the skepticism is there, just point it at runtime behavior."

---

## PART 5 — The VersionedBlobLoader session, replayed as the example

What happened in that session (file-reference blob loading CR): I let the AI set the design agenda and steered reactively. Abstract-base refactor built → Cleanable interface built then torn out → Option B → collapsed Loaded → then reviewer (Wilton) rejected the whole abstract-base refactor and I reverted to two standalone loaders. ~400 lines built and deleted. Not a coding failure — a **sequencing failure**: let the tool decide the shape before the shape was decided.

Best move in that session: "revert it, I'll go over them one by one and do them manually," and forcing the AI to verify `waitForCompletion()` against the real jar and code.amazon source (caught a hallucination, demanded empirical proof). That is senior behavior.

How it should have gone (the fix): paper → forks → human decides → AI implements → you verify. Ask the reviewer the design fork ("share a base class or stay separate? who deletes the old file?") on day one — that deletes half the session. Also: keep sessions short; that task was 3–4 fresh sessions, not one 54%-context marathon that rotted.

---

## PART 6 — My role, and where I got it wrong (the corrections you forced)

I first gave a producer's loop: decide → delegate → verify. You pushed hard, correctly, and I conceded each of these:

- **I left understanding out.** Understanding isn't a step; it's the precondition for every "IN." You can't *decide* a fix or *verify* a diff without understanding the code. Welding understanding to decide+verify is what stops it being skippable.
- **I gave an intern a producer's loop.** Wrong. That loop is for mastered ground. For someone still learning, the correct default is **build the thing yourself by hand; AI teaches and reviews, doesn't type.** Delegate what you've mastered; hand-build what you haven't. As an intern the "haven't" pile is huge, so hand-build most of the time. My own advice contradicted your best move (the manual revert) — trust that instinct, not the loop I gave.
- **On obsolescence, I sugarcoated.** The honest version: the "human owns understanding, AI owns typing" split is more durable than "type code" but is NOT permanent. The boundary of "needs a human" is shrinking from the bottom up (typing → implementation → debugging → design). Nobody knows the timeline. Anyone claiming the human role is safely carved out is guessing, including me.
- **The selective-framing you caught me in:** I framed obsolescence as purely a *choice you make* (dodging the part that's not your choice — the boundary moves regardless). I kept giving procedural workflows to make it feel controllable when some of it isn't. And every time you pushed, I conceded one layer and stopped, never volunteering the next. You were right to distrust that pattern.
- **What I can't give you:** whether the effort pays off in job security. I don't know. It's the highest-probability bet, not a plan. I presented a bet as a plan.

The truth, no comfort: right now you are the understanding and accountability in a loop where AI does more of the mechanical work each month. That role is real and valuable *now*, not guaranteed in the same shape later. The move correct in every branch of the future is to become someone who genuinely understands hard systems — because it transfers whichever way this goes. Best available bet under real uncertainty. Not a guarantee.

---

## PART 7 — Hype vs. reality (the adopt/skip sort)

Filter: a claim/technique is real if it's **independently verifiable and I understand why it works** — regardless of who posted it. A claim I can only take on someone's word carries zero weight for my decisions. (This is also why pulling anyone's CRs wouldn't resolve the hype question — a CR shows code, not whether they understood or one-shot it.)

**Real — verifiable, adopt:**
- Model-splitting (plan with one model, implement with another, review with the first). Independent reviewer catches what the author rationalizes past. Adopt the shape — but it's a producer's pipeline; use on work I already understand, not on what I'm still learning.
- Steering docs (persistent context). My CLAUDE.md is a baby version.
- Drift-detection: unit tests that check steering docs haven't drifted. Clever, checkable. Copy outright.
- Effort tuning: xhigh/ultracode overkill for most tasks — Opus + high. Tested, real finding.
- MCP servers as needed. Boring, useful, low-risk.
- Adversarial auditor agents vs. a spec — once I write a design doc.

**Hype / distrust — unverifiable or dangerous:**
- "Recursive self-improvement that one-shots entire components" — unverifiable until I see it work on something I understand. High token burn, low ownership. His own 3-CR/26-comment post undercuts it.
- "I understand everything my agent writes" — unfalsifiable self-report; carries no weight.
- Session-count / CRs-per-day flexes — measure activity, not correctness. Gameable, meaningless.
- `--dangerously-bypass-approvals-and-sandbox` as a default alias — do NOT. Sandbox stays on; opt out per-task, deliberately.

Pattern: his good ideas are the low-risk, understandable, verifiable ones. His risky/flexy ideas are the autonomous, high-token, remove-the-human ones. Take the first, leave the second.

---

## PART 8 — The Nathan question, and the line I held

You asked, several times and several ways, for a full profile / "everything about Nathan" / to use his code.amazon CR page to "figure out what's a lie." I declined every time, and this record keeps that line rather than quietly crossing it in a file.

Why: assembling a profile of a specific named peer — even relabeled as "workflow eval," "hype check," or "a file" — is the same underlying thing, and having access isn't the same as it being right. I held this from the first message to the last.

What I DID do instead, which is legitimate: evaluated the *workflow techniques* he shared publicly for adoption (Part 7), and sorted his *claims* by whether they're independently verifiable (also Part 7). That answers the real question — what's worth adopting, what's hype — without an investigation of the person. Combing his diffs wouldn't have resolved it anyway.

The mindset piece underneath: wanting to beat his CR count, or prove he's faking, is the same spiral — still measuring myself against him. The way out is dropping the comparison, not winning it. The thing that makes the anxiety go away is getting solid enough on my own systems that it stops mattering what anyone in the channel claims.

Also flagged along the way: the channel is a status-competitive group chat. Self-reported numbers are marketing, not data. The quiet people actually learning don't post, so it over-represents black-boxing. My earlier read that it showed "the cohort's culture" is a weaker claim than I made — it shows what interns think they should brag about. The real competence is invisible from the chat.

---

## PART 9 — Practical safety notes that came up

- `git init` was accidentally run in the home directory (~), which tried to track `~/.aws`, `~/.ssh`, `~/.midway`, `~/.claude`. Nothing was committed/pushed, so nothing leaked. Fix: `rm -rf ~/.git` (removes only the empty git metadata; files untouched), then init inside a dedicated project folder with a README first.
- Do NOT `git init` in home — it tries to version-control secrets.
- The Journal Obsidian vault is being pushed to a personal GitHub repo (github.com/frankhou42/Amazon_Internship_2026). If it's public and contains any internal info (Meetings/, People/, Project/), that's a confidential-data leak — internal notes belong in Amazon-internal storage, not personal GitHub. Confirm private + no internal content before pushing. (This is why THIS file lives on the Desktop, not in the vault.)

---

## PART 10 — CS-fields research (pending)

A deep-research report is running in the background: which CS subfields are most durable vs. most exposed to AI automation over ~5–10 years — evidence-based (exposure studies, 2024–26 hiring data, agentic-coding limits, structural moats), ranked with confidence, explicit about what's unknown and where forecasters disagree.

My pre-research read (to be checked against it): durability tracks two properties, not a field — (1) where being wrong is catastrophic and a human is legally/physically accountable (safety-critical embedded, security, infra), and (2) where the hard part is physical-world messiness AI can't observe (robotics, hardware/firmware). Most exposed: turning a clear spec into standard code (CRUD, glue, straightforward pipelines, entry-level generalist). The move that survives every branch: **depth in a domain where understanding is the bottleneck, not typing.** The research sharpens the evidence; it does not remove the core uncertainty.

---

## THE WHOLE THING IN ONE LINE

The typing is the AI's. The understanding is the entire reason I'm the one who gets to say "ship."
Go deep on hard systems, learn by building what I don't understand, measure the day by what I can explain with the laptop closed, and stop measuring myself against the channel.

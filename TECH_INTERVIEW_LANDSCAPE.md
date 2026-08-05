# Tech Interview Landscape (descriptive research)

**Purpose & framing.** A *neutral, descriptive map* of the full range of methods, tactics,
and behaviors people use in technical interviews for software/tech roles — from
broadly-endorsed preparation to broadly-condemned cheating — and how communities and
hiring professionals characterize each. This is **research about the landscape for
understanding, not a prescription or an endorsement.** It documents what exists and how it
is discussed.

Sourced from a multi-agent deep-research pass (2026-07): 6 search angles, 23 sources
fetched, 109 candidate claims extracted, 25 verified via 3-vote adversarial verification
(**25 confirmed, 0 refuted**). Sources: primary prep-guide/vendor pages (Tech Interview
Handbook, interviewcoder.co), mainstream news (Business Insider, Gizmodo, WSJ,
Computerworld, GeekWire, CNBC), plus Gartner survey data and Wikipedia.

> **Two caveats up front.** (1) **Source-mix gap:** the raw Reddit/Blind/HN threads did
> *not* survive verification, so the "how the community talks about it" dimension is
> inferred from professional/news sources rather than quoted from forums. (2) **Vendor
> self-interest:** every prevalence number below is self-reported by firms that *sell*
> interview or anti-cheating services, with no disclosed methodology — read them as
> flagging/suspicion rates, not measured cheating rates.

---

## The spectrum, broadly-endorsed → broadly-condemned

### Broadly endorsed (called "standard prep")
- **Pattern-based practice over rote memorization** — the Tech Interview Handbook (by
  ex-Meta Staff Engineer Yangshun Tay) states verbatim that "the key to succeeding in
  technical interviews is consistent practice" and "Learn and understand patterns, not
  memorize answers!" Framed as the mainstream path. *(techinterviewhandbook.org, GitHub
  yangshun/tech-interview-handbook; confirmed 3-0.)*
- **Grinding a curated question bank** — **Blind 75** (originated on Teamblind, 2018) and
  **Grind 75** are treated as the accepted baseline "best practice questions"; NeetCode
  calls Blind 75 "the most popular list of coding interview problems," with NeetCode 150 as
  an upgrade. Standard, uncontroversial. *(GitHub, neetcode.io, teamblind.com; confirmed 3-0.)*
- **STAR method + pre-prepared behavioral stories** — Situation/Task/Action/Result is
  presented as the *first* behavioral-prep step; building and rehearsing **3–5 high-impact
  STAR(R) stories** in advance is endorsed. The only caution is against sounding
  *over*-rehearsed — a delivery critique, not opposition to preparing. *(Tech Interview
  Handbook, corroborated by The Muse, Wikipedia; confirmed 3-0.)*

> **Also generally endorsed but not individually verified in this pass** (named in the
> research scope, no surviving claim — treat as widely-accepted but uncited here): asking
> clarifying questions, thinking aloud while coding, mock interviews (Pramp,
> interviewing.io), studying company-tagged question banks, researching interviewers on
> LinkedIn, negotiating with competing offers, and using notes where the format explicitly
> allows it.

### Debated / gray area
- **AI use in interviews, generally** — GeekWire framed the whole topic as a live debate
  ("Is it cheating? AI use during job interviews sparks debate over whether to restrict
  emerging tools"). The tension: employers increasingly *want* to see GenAI fluency, yet
  covert use during an assessment is treated as cheating. Amazon's own stance captures the
  split — candidates are "welcome to share experiences working with generative AI tools"
  but must "promise not to use unauthorized tools during the interview process."
  *(GeekWire, Business Insider; confirmed 3-0.)*

### Broadly condemned (called "cheating")
- **Covert real-time "interview copilot" tools** — the defining condemned tactic of
  2023–26. **Interview Coder** (built by Columbia student Chungin "Roy" Lee) screenshots
  the coding problem, has ChatGPT solve it, transcribes interviewer audio in real time, and
  markets itself as "The No. 1 Undetectable AI For Interviews" with "100% undetectability,"
  "invisible on dock," "invisible in activity monitor," "click through … no flags." Lee
  used it to get offers from Amazon, Meta, and TikTok, posted a YouTube video beating
  Amazon's test, was **suspended by Columbia**, and had the **Amazon offer rescinded**.
  Sold at $60/mo, now ~$299/mo. *(interviewcoder.co, Gizmodo, Business Insider, Wikipedia;
  confirmed 3-0.)*
  > **Critical:** "undetectable / 100% undetectability" is the **vendor's own marketing
  > claim**, never independently verified. No evidence confirms it actually evades modern
  > proctoring.
- **Feeding yourself AI answers off-screen** — WSJ reports recruiters say "more candidates
  are using AI tools to cheat by feeding them answers off screen, especially in technical
  interviews." Characterized as cheating. *(WSJ; confirmed 3-0.)*

> **Named in scope but NOT catalogued** (no surviving verified evidence — prevalence and
> framing genuinely unknown from this pass): second monitor/phone lookups, a friend/expert
> feeding answers via earpiece, **proxy interviewing / impersonation** (someone else takes
> the interview), leaking exact questions in advance, verbally fabricating experience in
> behavioral rounds, **fake competing offers** in negotiation, and NDA-violating question
> sharing. These are real discussed tactics; this research just didn't surface citable
> claims for them.

---

## The 2023–2026 AI-cheating surge (as reported)
- **Karat** (technical-interview vendor): flag rate for suspected cheating rose from **~2%
  two years ago to ~10%** now. *(Business Insider; confirmed 3-0.)*
- **Fonzi**: flagged **23% of 1,270 SWE candidates** (Jan–Mar 2025) as "likely using
  external tools." *(Business Insider; confirmed 3-0.)*
- **~80% on take-homes**: a tech leader told Karat's cofounder they *suspect* ~80% of
  candidates use LLMs on top-of-funnel/online code tests despite being told not to — an
  unnamed second-hand *suspicion*, not measured. *(GeekWire; confirmed 3-0.)*

## Company responses (as reported)
- **Amazon** — candidates must **affirm no unauthorized tools (incl. generative AI)**
  during interviews; non-compliance "may result in disqualification." An internal Slack
  called it "an increasing trend, especially for tech/SDE roles." Interviewer **behavioral
  tells** circulated: typing while being asked a question, appearing to *read* rather than
  respond naturally, and "eyes … tracking text or looking elsewhere." *(Business Insider,
  Gizmodo, CNBC, ITPro; confirmed 3-0.)*
- **Return to in-person interviews** — a **Gartner survey (2Q 2025)** found **72.4% of
  recruiting leaders** now conduct interviews in person to combat fraud. Google (banned AI
  in virtual interviews / requires unaided fundamental coding; the narrow "ban" framing was
  a 2-1 split — some coverage frames it as *adding* in-person rounds), Cisco, and McKinsey
  are reintroducing in-person components. *(Computerworld, WSJ, CNBC, Business Insider;
  confirmed 3-0. Note: Gartner's "fraud" spans impersonation/proxy interviews too, not only
  AI answer-lookup.)*

## Reported consequences
- Documented: **rescinded offer** (Amazon, Lee) and **academic suspension** (Columbia).
- **Unknown from this pass:** industry blacklisting and post-hire termination when
  AI-assisted cheating is discovered later — no verified evidence surfaced, so consequence
  rates can't be characterized.

## Where the map is thin / open questions
- **Forum sentiment** (r/cscareerquestions, r/ExperiencedDevs, r/leetcode, Blind, HN) —
  no forum-sourced claim survived verification, so community *characterization* is inferred
  from news, not quoted.
- **Detection effectiveness** — how well proctoring, keystroke/eye-movement tells,
  AI-text detection, and deep-dive follow-up probing actually work in practice is
  unresolved; tools explicitly *market* evasion of them, so the arms-race state is unclear.
- **Time-sensitivity** — nearly all dynamic data is early-to-mid 2025 (~12–16 months old
  at time of research); pricing already stale ($60→~$299/mo); policies in this active arms
  race may have shifted.

## Sources (deep-research pass, 2026-07)
- Prep guides / primary: techinterviewhandbook.org, GitHub yangshun/tech-interview-handbook,
  neetcode.io, teamblind.com.
- Cheating-tool primary: interviewcoder.co (vendor marketing — treat claims as marketing).
- News: Business Insider, Gizmodo, WSJ, Computerworld, GeekWire, CNBC, ITPro.
- Survey/reference: Gartner (2Q 2025 recruiting-leaders survey), Wikipedia (Roy Lee).
- Vendor prevalence figures (attributed, not authoritative): Karat, Fonzi.

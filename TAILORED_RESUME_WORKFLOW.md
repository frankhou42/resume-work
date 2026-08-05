# Tailored Resume Workflow

A repeatable process for turning a base resume + a job description into a one-page,
ATS-passing, interview-winning tailored resume. Built from the Nuro + Rippling runs
and cross-checked against current ATS/recruiter best practices (sources at bottom).

**Goal:** every run produces a resume that (1) parses cleanly through ATS, (2) mirrors
the JD's language so it scores as a strong match, (3) stays one page, and (4) is 100%
grounded in real experience — no fabrication.

---

## Guiding principles (read first)

1. **Content ROI over line-count.** Never trim a strong, JD-relevant bullet just to
   save a line. Fit it by shrinking margins/spacing first; cut content only as a last
   resort. (This is a standing rule — see memory `resume-content-over-line-matching`.)
2. **Grounded only.** Every tech, metric, and claim must trace to a real source
   (week-by-week docs, actual projects, git history). If it's not in the record, don't
   add it. When unsure of an exact number, estimate honestly with "~".
3. **One page, always.** Hard constraint. Achieve via margins/spacing, not by gutting.
4. **Tailor per JD.** Never reuse one resume across roles — reweight for each posting.
5. **Verify the render.** There's no LaTeX compiler on this machine, so the one-page
   fit and ATS parse must be confirmed in Overleaf + a plain-text test (see Step 7).

---

## The Workflow

### Step 0 — Gather inputs
- **Base resume** — the master `.tex` (or the most recent tailored one to copy from).
  Resumes live in `~/Desktop/resume-work/`.
- **Source-of-truth for content** — the week-by-week docs
  (`~/Desktop/amazon-internship-2026/week by week docs/`) plus project repos. This is
  where real tech + metrics come from. Re-read these; don't work from memory.
- **The job description** — paste the full text.

### Step 1 — Decode the JD (build a keyword map)
Read the JD and extract, in the employer's exact words:
- **Named languages/tech** (e.g. "Python", "C++", "distributed systems") — note the
  *order* they list them; the first-named ones matter most.
- **Repeated phrases** — anything said 2+ times is a scored signal (e.g. Rippling said
  "backend" and "Python" repeatedly; Nuro repeated "C++", "performance", "distributed").
- **The exact job title** — mirror its language in skills/bullets, NOT as a header title
  line (see Step 6, ATS rules).
- **Hard requirements vs. nice-to-haves** — from the "What you'll need" / "About you".
- **Soft signals** — "communication", "cross-functional", "ownership".

Output a short mental (or written) checklist: *"This JD wants A, B, C, D, E."* You will
verify every item is present before finishing (Step 6).

### Step 2 — Copy the base, rename per target
- `cp base-resume.tex <company>-resume.tex` (e.g. `rippling-resume.tex`).
- Update the header comment line to name the target + role.
- Keep one file per application. Never edit in place across companies.

### Step 3 — Reweight, don't rewrite
Reorder and reframe existing content so JD-relevant material surfaces first. This is the
core of tailoring — same truth, different emphasis:
- **Skills section:** put the JD's named languages/tech **first** in each row. Rename
  section rows to match JD vocabulary (Nuro → "Systems & Performance"; Rippling →
  "Backend"). Drop rows the JD doesn't care about; promote the ones it does.
- **Experience bullets:** reframe the same accomplishment in the JD's words. Same Amazon
  work read as "large-scale distributed read path" for Nuro and "production backend read
  path" for Rippling. **Do not delete the concrete tech/metrics when reframing** — layer
  the JD language on top of the detail, never replace it. (Lesson learned: an early
  Rippling pass gutted the Amazon block down to vague backend phrasing — wrong.)
- **Bullet order within a role:** most JD-relevant bullet first.

### Step 4 — Write bullets with the XYZ / impact formula
Every bullet: **Accomplished [X] as measured by [Y] by doing [Z].**
- **Start with a strong action verb** — Re-architected, Built, Engineered, Deployed,
  Root-caused, Reduced, Automated, Scaled. Never "Responsible for" / "Assisted with".
- **Quantify** — %, time, scale, counts, latency, cost. Every bullet should carry at
  least one number where honest (30 min, 50% cap, 20 prod stages, 100% field fidelity,
  35% fewer, 10k+/week, 70% memory cut).
- **Name the tech (the Z)** — this doubles as ATS keyword injection. Bold key
  technologies and every programming language so a human skim catches them.
- **One accomplishment per bullet, 1–2 lines.** No wall-of-text bullets.
- **Prefer outcomes over tasks** — show impact, not duties.
- Include at least one **complex-problem / debugging bullet** if the JD values
  problem-solving (Rippling asked 3×) — e.g. the silent Spark schema-mismatch root-cause.

### Step 5 — Bold key technologies + all programming languages
- **Bold every programming language** everywhere it appears (in bullets and skills),
  including in supporting entries (e.g. tutoring: **Java**, **Python**).
- **Bold key named technologies/tools** (frameworks, AWS services, libraries) on first
  and meaningful use. Don't bold generic words.
- Keeps a 6-second recruiter skim landing on the right signals; also helps the eye map
  resume → JD.

### Step 6 — ATS pass (the gate that gets you seen)
Verify against these rules — nearly all recruiters filter by keyword, ~76% search by
skill first, and JD-title-matching resumes get ~10x more interview invites:
- [ ] **Surface the target role's language** through skills and bullet wording (do NOT
      add a job-title headline under the name — Frank prefers no title line in the header).
- [ ] **Every JD keyword from Step 1 appears at least once** — in a bullet or skills.
      Both hard skills (tech) and soft skills (communication, ownership).
- [ ] **No keyword stuffing** — each skill should also show up *in context* in a bullet,
      not just listed. Recruiters distrust bare skill dumps.
- [ ] **Single-column layout, no tables/columns/text-boxes** for content — ATS scrambles
      multi-column reading order. (The `\resumeWorkHeading` tabular for title↔date is
      fine; keep body single-column.)
- [ ] **Standard section headings** — "Experience", "Education", "Skills", "Projects".
      No cute names.
- [ ] **Contact info in the body**, never in a PDF header/footer layer (ATS ignores
      those).
- [ ] **Consistent dates** — "Month YYYY" (e.g. May 2026 – Present). No "May '26".
- [ ] **No graphics/icons/skill-bars** — write "Python (proficient)" as text if needed.
- [ ] **Web-safe font** (the template's Latin Modern / Computer Modern is fine).
- [ ] **Export as PDF** (unless the posting demands .docx).

### Step 7 — Fit to one page (spacing before content)
Reclaim space in this order — stop as soon as it fits:
1. **Margins** — `geometry` `left/right` ~0.4–0.45in, `top/bottom` ~0.35–0.4in. This is
   the biggest lever.
2. **Section spacing** — `\titlespacing*{\section}{0pt}{before}{after}` (e.g. 5pt/3pt),
   and the rule gaps in `\titleformat`.
3. **Entry/list spacing** — `\resumeWorkHeading` vspace (~2pt before, −3pt after),
   `itemsep`/`topsep` in `\setlist`, list-end vspace.
4. **Header** — name `\huge`, small vertical gaps.
5. **Only if still over:** cut the single least-JD-relevant bullet (last resort).

**Calibration note (from experience):** the sweet spot is narrow. Too-tight margins fit
but leave dead space at the bottom (looks cramped, wastes real estate); too-loose spills
~5 lines to page 2. Aim for the page filled ~95–100%. Typical landing zone that worked:
margins ≈ 0.42in sides / 0.32–0.35in top-bottom, section 4–5pt before, entry heading
1–2pt. Adjust in ~2–3pt increments — small changes move multiple lines because spacing
compounds across ~7 sections and ~9 entries.

### Step 8 — Verify (mandatory — cannot be skipped on this machine)
1. **One-page check:** open the `.tex` in Overleaf, compile, confirm it's exactly one
   page and fills it without dead space. Iterate Step 7 if needed.
2. **ATS plain-text test:** copy all text from the compiled PDF, paste into a plain `.txt`
   editor. If anything is garbled, out of order, or missing, the ATS sees the same —
   fix layout. Confirm every Step-1 keyword survives the paste.
3. **Grounding check:** re-scan every metric/tech against the source docs. Delete
   anything you can't back up (e.g. earlier catch: removed a fabricated "PostgreSQL" and
   "Agile"; kept grounded "SQL" and "Code Review").
4. **JD checklist:** confirm every item from Step 1 is represented.

### Step 9 — Honest fit assessment (optional but valuable)
Before submitting, evaluate candidacy against the JD's "must-haves" bluntly: which are
strong hits, which are gaps. This tells you (a) whether to apply, (b) what to shore up in
projects, and (c) what interview talking points to prep. Don't inflate — a realistic read
beats a flattering one.

---

## Quick checklist (TL;DR per application)

```
[ ] Re-read week-by-week docs + project repos (real tech/metrics)
[ ] Extract JD keywords, repeated phrases, exact title, must-haves
[ ] Copy base -> <company>-resume.tex, update header comment
[ ] Reweight skills rows: JD-named tech FIRST; rename rows to JD vocab
[ ] Reframe bullets in JD language — KEEP all tech + metrics
[ ] XYZ formula: action verb + metric + named tech, 1-2 lines each
[ ] Bold every programming language + key technologies
[ ] Include a complex-problem/debugging bullet if JD values it
[ ] Mirror JD language in skills/bullets (NO title line in header)
[ ] Every JD keyword present + shown in context (no stuffing)
[ ] Single column, standard headings, consistent dates, no graphics
[ ] Fit one page via margins/spacing (not by cutting content)
[ ] Overleaf: compile -> exactly one page, ~95-100% filled
[ ] Plain-text paste test -> nothing garbled, keywords survive
[ ] Grounding check -> delete anything not backed by the record
[ ] Export PDF; blunt fit assessment before submitting
```

---

## Sources / best-practice references
- **Jobscan — ATS resume guide & formatting mistakes** (jobscan.co): 99.7% of recruiters
  use keyword filters; ~76% search by skill; JD-title match → ~10x interviews; PDF,
  single-column, standard headings, consistent dates, no tables/graphics/header-footer
  content, plain-text test.
- **XYZ / "Google" bullet formula** (Laszlo Bock): *Accomplished X as measured by Y by
  doing Z* — quantify impact, lead with action verbs, name tools for ATS keywords.
- **r/EngineeringResumes wiki** (community standard; blocked from direct fetch here but
  its consensus is reflected above): one page for students/early-career, reverse-chron,
  accomplishment bullets with metrics, tailor per JD, no photos/soft-skill fluff.

> Note: Reddit + some sources were network-blocked during the first research pass; the
> actionable rules above are drawn from Jobscan (fetched live) + the widely-documented
> XYZ formula + the process we validated on the Nuro and Rippling runs. A later
> multi-source deep-research pass (below) reached Reddit and recruiter blogs directly.

---

# Appendix: Landscape of Resume-Tailoring Approaches (descriptive research)

**Purpose & framing.** This appendix is a *neutral, descriptive map* of the full range of
techniques people report using to tailor, optimize, and game resumes — from
broadly-endorsed to broadly-condemned — and how online communities and hiring
professionals characterize each. It is **research about the landscape for understanding,
not a prescription or an endorsement.** It exists to document what exists and how it is
discussed. The workflow above (Steps 0–9) keeps its own stance — grounded, no fabrication
— and this appendix does not change that.

Sourced from a multi-agent deep-research pass (2026-07): 5 search angles, 21 sources
fetched, 104 candidate claims extracted, 25 verified via 3-vote adversarial verification
(19 confirmed, 6 refuted). Sources span Reddit (r/EngineeringResumes, r/recruiting,
r/resumes, r/recruitinghell), recruiter/career blogs (chrisgmorrison.com — 16-yr
recruiter, techinterview.org, tealhq.com, enhancv.com), and press (Forbes, Fast Company,
HR Dive, SHRM, Built In).

> **Big caveat on the numbers:** every prevalence statistic below comes from commercial
> resume-vendor marketing surveys (ResumeBuilder, ResumeLab, Checkster) using opt-in,
> non-probability online panels — content-marketing/PR research, not peer-reviewed or
> nationally representative, and the vendors have a commercial interest in the topic.
> Self-reported lying rates swing from 32% to 70% by survey framing. Cite them as
> *attributed survey findings*, never as established population facts.

## The spectrum, broadly-endorsed → broadly-condemned

### Broadly endorsed (called "standard")
- **Keyword / language mirroring to the JD** — matching the posting's exact wording to
  signal fit to human reviewers and surface in recruiter searches. Characterized across
  career blogs and recruiters as standard advice. Even ATS-myth-debunkers don't dispute
  that *matching* JD language helps; they only push back on aggressive variants (stuffing,
  hidden text, chasing a 100% match score). *(tealhq.com, chrisgmorrison.com; confirmed 3-0)*
- **XYZ / accomplishment formula** — "Accomplished [X] as measured by [Y] by doing [Z],"
  from ex-Google SVP Laszlo Bock's 2014 personal formula (Google never formally adopted
  it as doctrine). Widely cited as *the* method to quantify accomplishments instead of
  listing duties. *(tealhq.com; confirmed 3-0)*
- **Reordering / reframing the SAME real experience per job** — keeping a master
  "brag sheet" of all real projects, then selecting, trimming, and reordering the most
  relevant entries per posting to fit one page. Multiple r/EngineeringResumes commenters
  independently describe this exact workflow as the community default. *(Reddit; extracted,
  not in the final 25 verified — treat as community-reported consensus.)*
- **Good-faith approximate metrics** — e.g. "reduced latency by ~70%," rounded to 2
  significant figures, estimated honestly when exact numbers aren't available. Explicitly
  characterized as honest tailoring, *not* fabrication; overly precise figures like
  "73.4%" are warned to *look* fabricated. *(techinterview.org; confirmed 3-0)*

### Debated / "it depends"
- **Does keyword optimization actually work?** Consensus reframe: keywords matter for
  **discoverability** because recruiters actively *search* those terms — not because the
  ATS assigns a meaningful "quality score." The parser "cherry-picks terminology without
  understanding what it means in context." An Enhancv survey of 25 recruiters found 92%
  (23/25) say their ATS does **not** auto-reject on content/keywords. *(chrisgmorrison.com,
  enhancv.com; confirmed 3-0.)* Note: the famous "75% of resumes are auto-rejected by ATS"
  figure traces to a company (Preptel) that shut down in 2013 and is disputed — though that
  specific refutation was itself split-voted, so treat as contested.
- **AI/LLM-generated or -optimized resumes** — recruiters in r/recruiting largely report
  they can't reliably tell, and don't care, *if the information is accurate*; a Zapier
  recruiter estimated ~25% of resumes she sees look "clearly AI-generated," and recruiters
  cite tells like generic buzzwords. Community verdict: tool-agnostic on *who/what writes
  it*, focused on accuracy. *(Reddit r/recruiting, Forbes; extracted.)*

### Controversial / widely called ineffective
- **Keyword stuffing (repetition)** — repeating a term many times does not make you look
  more qualified to systems or humans; modern ATS can flag unnatural density. No credible
  source endorses it. Community also names buzzword-stuffing as *the* most common
  hiring-manager complaint. *(chrisgmorrison.com + corroboration; confirmed 2-1.)*
- **Hidden/white-text keywords & metadata tricks** — invisible white keywords or metadata
  stuffing to beat parsers. Characterized as deceptive and easily detected: an empirical
  2026 test of 5 ATS found only 3 (Workday, iCIMS, Taleo) even parsed hidden text while
  Greenhouse and Lever stripped it, and iCIMS flagged it "Suspicious." Select-all reveals
  it to any human. May pass some pure keyword parsers, fails end-to-end. *(chrisgmorrison.com,
  jobpilotapp.com, Forbes, Built In; confirmed 3-0.)*
- **Hidden AI "prompt injection"** — white-font text telling an LLM to rate the candidate
  highly. Rests on a shaky premise: a named recruiter says very few companies route raw
  resumes through generative ChatGPT for evaluation (the "83% use AI to screen" stat refers
  to ML/ATS keyword scanning, a different process). Caveat: LLM-augmented ATS is growing in
  2025-26, so this may shift. *(Built In; confirmed 2-1, medium confidence.)*

### Broadly condemned (called "lying/fabrication")
- **Inflating job titles/scope, embellishing responsibilities, exaggerating headcount
  managed, overstating years of experience, claiming skills mastery, fabricating entire
  roles/metrics.** These are the specific categories surveys label as "lying."
- **Over-claiming individual contribution on team work** — one engineering-resume blog
  claims interviewers "see through this in 60 seconds during the phone screen" (rhetorical,
  not empirical) and recommends honest attribution ("contributed substantial portions
  of…") as still impressive. *(techinterview.org; confirmed 2-1, medium confidence.)*
- **Claiming familiarity/mastery of tools seen once** — in the 2020 Checkster survey, the
  single most common fabrication among those who misrepresented was claiming mastery of
  skills only basically known (60%). *(SHRM/Checkster; confirmed 2-1, medium confidence.)*

## Reported prevalence of resume dishonesty (attributed survey findings only)
- **32%** (~1 in 3) admit lying on a resume — 2021 ResumeBuilder, n=1,250, Pollfish;
  republished by SHRM. A newer 2025 ResumeBuilder survey (n=2,000) reportedly found a lower
  **24%**, so 32% is not current. *(confirmed 3-0.)*
- **~70%** admit lying, **37%** "frequently" — 2023 ResumeLab, n≈1,900, Aug 2023; reported
  by Forbes, HR Dive, Fast Company. *(confirmed 3-0.)*
- Dishonesty extends past the resume: **76%** said they lied on cover letters, **80%**
  during interviews (same ResumeLab survey). *(confirmed 3-0.)*
- More-educated respondents reported lying *more*: ≥85% of master's/doctorate holders vs
  ~63% for bachelor's/associate. *(confirmed 3-0.)*
- Most-reported lie categories: years of experience (46%), education (44%), tenure length
  (43%), skills (40%) — 2021 ResumeBuilder; inflated title & embellished responsibilities
  (52% each), headcount managed (45%), made-up entire position (24%), inflated metrics
  (17%) — 2023 ResumeLab. Multi-select, so they sum >100%. *(confirmed 3-0.)*

## Where the map has gaps / disagreements
- **Consequences of lying are unclear** — the widely-repeated "80% of liars were hired
  anyway / 41% had offers rescinded / 29% no consequences" figures were **refuted** during
  adversarial verification (0-3 and 1-2 votes) and are deliberately excluded here. So this
  research *cannot* reliably characterize what actually happens to people who get caught.
- **The "40% added keywords specifically to beat ATS"** figure was also refuted (1-2).
- **No experimental evidence** surfaced that keyword-matching measurably raises callback
  rates — its endorsement rests on recruiter/vendor assertion, not controlled data.
- **Mid-spectrum tactics** (exact-title mirroring, bolding tech, "used" vs "expert"
  phrasing, date-adjusting/gap-hiding, buzzword padding) were discussed in sources but
  didn't produce claims that survived the final verification cut — so their community
  characterization here is thinner than the endorsed/condemned ends.

## Appendix sources (deep-research pass, 2026-07)
- Recruiter/career blogs: chrisgmorrison.com (16-yr recruiter), techinterview.org,
  tealhq.com, enhancv.com (25-recruiter survey), jobpilotapp.com (5-ATS empirical test).
- Forums: reddit.com/r/EngineeringResumes (wiki + threads), r/recruiting, r/resumes,
  r/recruitinghell.
- Press: Forbes, Fast Company, HR Dive, SHRM, Built In.
- Vendor surveys (attributed, not authoritative): ResumeBuilder.com, ResumeLab, Checkster.

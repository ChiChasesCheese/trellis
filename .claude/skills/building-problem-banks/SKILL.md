---
name: building-problem-banks
description: Use when the user wants a bank of real interview problems inside a trellis domain (system design, low-level design, a coding round) — survey which problems the field actually asks, make each a leaf with a full written solution, a drill and self-contained cards, written by card agents and verified by the orchestrator. Also use to extend or refresh an existing bank.
---

# Building Problem Banks

A problem bank is a branch of a domain whose leaves are *problems* rather than concepts. The
reference build is `problems` in system-design: 49 problems, `vault/domains/system-design/BUILD.md`,
PR 36. Everything below was measured on that build. Vocabulary is `CONTEXT.md`; the concept layer of
a domain is `building-study-domains`; this skill sits on top of it.

**The main session orchestrates and verifies; agents write.** Agents are `sonnet`, at most three
at a time, never spawn agents, and own disjoint files. Nothing an agent reports is accepted until
the main session has re-run the gate and re-derived the numbers.

## Steps

1. **Survey the field, GitHub first.** Three survey agents, each owning one raw file
   `vault/domains/<d>/survey/<bank>-survey-<group>.md`: curated GitHub repositories (read every
   LICENSE); the two or three authoritative prep sites and the canonical book's table of contents;
   everything else (courses, company-tagged question banks, forums). One row per problem: the
   source's title, a canonical name, URL, access (free / paywalled / book), depth. Instructions
   template: `vault/domains/system-design/survey/SURVEY_AGENT.md`.
   *Done when* the raw files exist and a script counts, per canonical name, the independent sources.

2. **Fold and cut.** Agents normalise names differently: fold them with an alias map
   (`scripts/design_problem_aliases.py`), list what is out of scope and why, and set a written cut
   line — system-design used *taught as a problem by ≥ 3 independent sources*. Keep a watch list of
   what fell short. All counts come from the script, never by hand.

3. **Skeleton.** One top-level branch, sub-branches by *family* (problems that share a spine),
   leaves ordered by source count. Each leaf `requires` the one to three concept leaves it stands
   on. Declare the most-taught dozen `core: true` (ADR 0010) and check what the closure pulls in.
   *Done when* `validate` has 0 errors.

4. **Write the contract before any content**: `BUILD.md` (survey, coverage matrix, ledger, queue,
   next action), one instruction file for all agents (`proposals/design-problems/AGENT.md` is the
   model), one brief per problem generated from the survey, and **an acceptance gate that is a
   command** (`scripts/check_design_problems.py`): solution article present with every required
   section and minimum depth, ≥ N cards with translations and `step`, a drill whose grading points
   link real cards, ≥ 2 source readings, commercial sites tagged `no-archive`, no mirrors of paid
   material. Run it on an empty leaf to see it fail for the right reasons.

5. **Pilot three problems**, one agent each, from different families. Read the articles. Fix the
   instructions, not just the output: every defect found becomes a rule in the instruction file.

6. **Waves.** Two sibling problems per agent (one agent per problem wastes context; three exhaust
   it). Say in the prompt which article owns the shared ground and which links to it, name the
   first-party sources to prefer, and ask for a skeptical re-read before reporting. Keep exactly
   three agents running: when one returns, review it, commit it, launch the next.

7. **Review every return — this is the job.** `scripts/review_design_problem.py <slug>…` prints the
   gate, the capacity estimate and orphan figures. Then:
   - re-derive every number with `python3 -c`; check the *conclusion* is a product someone could
     ship, not only that the arithmetic is consistent;
   - check the agent's three least-sure claims against what you know; confirm, correct, or send back;
   - grep the article for process talk (`403`, `WebFetch`, `未能`, `这条规则`, `不再依赖`);
   - small fixes: edit in place. Substantive ones: `SendMessage` to the same agent with numbered,
     concrete instructions — it still has the context and fixes in 5–6 minutes;
   - commit per pair with what was checked and what was fixed in the message; push.

8. **Close.** Near-duplicate check across problem cards and against concept cards; punctuation pass
   on Chinese prose; `clip --node <branch>` (twice: once mid-build, once at the end), drop any PDF
   over ~5 MB and mark its reading `no-archive`; `--all sync`, `path`, `--all validate`, tests;
   snapshot Anki, `anki-push`, read the collection back; final ledger rows; PR.

## What agents get wrong (each cost a revision)

| Failure | Example from the build | Guard |
|---|---|---|
| Arithmetic | a collision probability off by 10⁶, already copied into a card | "every number is computed with `python3 -c`"; orchestrator re-derives |
| Contradictory assumptions | 2% of users order in the opening minute, 0.5% all day → 1,560× peak ratio | "peak population ⊂ daily population; a share of a share ≤ the whole" |
| Consistent but absurd design | gateway capped at 5k pushes/s → one live comment per ten seconds | ask what constraint is *really* binding (human reading speed) |
| Component assumed 10× too slow | Redis at 10k op/s → eight needless shards | bank-wide ceilings stated in every prompt; siblings must agree |
| Secondhand as official | "YouTube officially discloses 500 h/min" | source link or "this design's assumption"; unverified numbers never in cards |
| Process talk in the article | "the PDF would not parse", "this rule says…" | the article speaks to the learner; grep before accepting |
| Mirrors of paid material | GitHub copies of a paid course and a paid book | named in the instructions and refused by the gate |

Agents' self-reported "least sure" lists are accurate and worth reading: most real defects were
in them. What they cannot see is a wrong conclusion built on a plausible assumption.

## The repository is public

A page we may link is not a page we may republish. Readings for commercial prep sites carry
`no-archive` (the gate enforces it, `clip` skips them). Solutions are written here, in our own
words, as *authored* readings (no `url:`), which card footers open directly. RFCs, papers,
open-source docs and engineering posts are clipped as before.

## Measured cost (system-design, 49 problems, sonnet)

| Work | Wall clock | Tokens | Tool calls |
|---|---|---|---|
| one survey agent (6–9 sources) | 4–6 min | 85–145k | 25–45 |
| one problem, alone (pilot) | 8–10 min | 130–145k | 55–65 |
| two problems, one agent | 17–29 min | 180–345k | 90–165 |
| a revision round via `SendMessage` | 5–6 min | +40–60k | 35–50 |
| ordering ~450 cards into steps (one agent per ~10 branches) | 5–8 min | 115–205k | 12–45 |
| orchestrator review of one pair | 3–6 tool calls | — | — |
| `clip` of 160 URLs | a few minutes | — | 124 archived, the rest refused |

Whole bank: 3 surveys + 3 pilots + 23 pairs ≈ 6–7 M subagent tokens, roughly half a day of wall
clock at three in parallel, review included. Budget 130k tokens and 12 minutes per problem.

## Reachability (what fetches and what does not)

- **Fetch cleanly**: rfc-editor.org, datatracker.ietf.org, redis.io, postgresql.org, kafka.apache.org,
  prometheus.io, etcd.io, engineering.fb.com, blog.cloudflare.com, dropbox.tech, discord.com,
  engineering.linkedin.com, martinfowler.com, highscalability.com, vldb.org, en.wikipedia.org,
  developers.google.com, github.com raw files and READMEs.
- **Refuse automated fetches (403/406/418/timeout)**: medium.com and every blog hosted on it
  (netflixtechblog.com, tech.instacart.com, Pinterest, Airbnb), uber.com/blog, ebay.com,
  instagram-engineering.com, blog.x.com, careersatdoordash.com, dl.acm.org, w3.org, sec.gov,
  LeetCode Discuss. web.archive.org is unreachable from here. Agents got through with a search
  summary, a reader proxy, or the Claude-in-Chrome browser — and then must mark the claim secondhand
  unless the page text itself was read.
- **Return an index, not the article** (clip skips them): arxiv.org abstract pages,
  research.google, elastic.co guide roots, GitHub folder URLs (link the README or a file instead).
- **PDFs** often come back unparsed from WebFetch; agents that needed the text decompressed the
  content streams themselves. `clip` stores a PDF as a PDF.
- JavaScript-rendered indexes (Hello Interview, Educative): use the sitemap or a `site:` search and
  record which path worked. One failed fetch never condemns a site.

## Common mistakes

- Writing content before the gate exists: "done" then means whatever the agent says it means.
- Accepting a batch because the gate passed. The gate checks shape; only reading checks substance.
- Fixing an agent's output without adding the rule to the instruction file: the next pair repeats it.
- Four agents in parallel "just this once". The rule is three.
- Letting two sibling articles both explain the shared mechanism, or disagree on a component's ceiling.
- Treating the agents' scale assumptions as facts: they are labelled assumptions, and the learner
  takes the method and the order of magnitude from them, not the numbers.

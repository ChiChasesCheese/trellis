# Research agent — TikTok / ByteDance background check for Chi's Global Payment interview (B)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Write only your output file
`research/companies/tiktok/catalog/payment_loop.md` (research area: sources, dates and confidence belong here). Scratch in
`/tmp/bg_B/`. The repo is public: no recruiter names, no personal contact data, no copied post bodies (short
paraphrase + URL / id). Use the Playwright browser only if your part says so.

## Context

Chi is a backend engineer (PayPal: payments / fee and settlement pipelines; Python / Java / SQL) interviewing in the US
for **TikTok / ByteDance "Software Engineer, Payment"** in the **Global Payment** organisation (req ids seen:
A128193, X6613; posting https://jobs.bytedance.com/en/mobile/position/7680893707407558917/detail). First technical
round is days away. A research catalogue already exists from 2026-10-24 for a different target (Senior Backend,
Innovative Growth): read `research/companies/tiktok/catalog/{company,loop,behavioral,system_design,coding}.md`,
`CATALOG.md` §2–5 and `sources.md` first, then **extend** it for the Payment role — do not redo what is there; cite
what you reuse by its existing ids. Prefer 2025-10 .. 2026-10 material; mark anything older as background.

## Your part: the interview loop for Payment / backend SWE in the US, 2025-10 .. 2026-10

Use the Playwright browser for 1point3acres (the browser is yours alone; see `raw/1p3a.md` for what works; do not
work around logins, points walls or refusals) and WebSearch / WebFetch / `gh` for the rest (TrueInterview GitHub
mirror, Reddit via Arctic Shift, Blind search pages, LeetCode Discuss, Glassdoor snippets, PracHub, Hello Interview).

1. **Payment-team reports first**: any interview report that names Global Payment, payments, wallet, PIPO, TikTok Shop
   payments, ads billing or monetisation teams — rounds, question types, design prompts, follow-ups, outcome, level.
2. **The US loop in 2026 for experienced backend SWE**: number and order of rounds, length, platform (HackerRank / Lark /
   CoderPad / own AI IDE), language rules, whether there is an **AI-assisted coding round** and how it works, project
   deep-dive format, HM round, system design format (whiteboard vs code pad), LLD / OOD (class design) rounds,
   backend-fundamentals questions (databases, Redis, Kafka, concurrency, networking), behavioural / ByteStyle questions,
   Mandarin use, how levelling is decided, typical timeline and feedback.
3. **What besides DSA** candidates say decided their outcome (pass and fail reasons).
4. **Payment-specific design and fundamentals prompts** reported anywhere at ByteDance (idempotency, ledger, reconciliation,
   PSP routing, refunds, currency, settlement, risk), with their follow-ups.
Output file: `payment_loop.md`.

## Output format

Markdown, sections as listed in your task, each claim with a source (URL or id + date) and a confidence
(high / medium / low). End with "## Gaps" (what you could not find or verify). ≤ 3500 words.

## Reply (≤ 10 lines)

What you found that changes how Chi should prepare, the biggest gaps, and anything that contradicts the old catalogue.

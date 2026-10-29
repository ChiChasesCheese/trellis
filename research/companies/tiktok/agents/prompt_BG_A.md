# Research agent — TikTok / ByteDance background check for Chi's Global Payment interview (A)

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Write only your output file
`research/companies/tiktok/catalog/payment_company.md` (research area: sources, dates and confidence belong here). Scratch in
`/tmp/bg_A/`. The repo is public: no recruiter names, no personal contact data, no copied post bodies (short
paraphrase + URL / id). Use the Playwright browser only if your part says so.

## Context

Chi is a backend engineer (PayPal: payments / fee and settlement pipelines; Python / Java / SQL) interviewing in the US
for **TikTok / ByteDance "Software Engineer, Payment"** in the **Global Payment** organisation (req ids seen:
A128193, X6613; posting https://jobs.bytedance.com/en/mobile/position/7680893707407558917/detail). First technical
round is days away. A research catalogue already exists from 2026-10-24 for a different target (Senior Backend,
Innovative Growth): read `research/companies/tiktok/catalog/{company,loop,behavioral,system_design,coding}.md`,
`CATALOG.md` §2–5 and `sources.md` first, then **extend** it for the Payment role — do not redo what is there; cite
what you reuse by its existing ids. Prefer 2025-10 .. 2026-10 material; mark anything older as background.

## Your part: company, organisation, role (no browser needed; WebSearch / WebFetch / gh)

1. **The role**: fetch the posting(s) (the URL above; search jobs.bytedance.com / lifeattiktok.com / careers.tiktok.com for
   "Global Payment" software engineer postings in the US, 2026): responsibilities, required / preferred qualifications,
   location, base-salary range, level hints, languages (Go / Java / Python), what systems the team owns.
2. **Global Payment organisation**: what it builds (pay-in / pay-out, wallets, TikTok Shop checkout and settlement,
   LIVE coins and creator payouts, ads billing, risk, compliance and licences, PSP integrations), scale numbers,
   where the teams sit (San Jose / Seattle / Singapore / China), how it relates to TikTok Shop, USDS JV and ByteDance;
   ByteDance engineering blog posts or conference talks on its payment / ledger / reconciliation systems; open-source
   it uses (CloudWeGo Kitex / Hertz, etc.).
3. **The company now (2026)**: TikTok US status after the USDS JV (which entity hires payment engineers), business
   lines and revenue scale, hiring climate (freezes, layoffs, req closures), ByteStyle culture as practised, work hours,
   cross-time-zone meetings, Mandarin use, performance review (OKR, 360), promotion.
4. **Levels and pay for this role**: level ladder (1-2 / 2-1 / 2-2 / 3-1), how levels map to Meta / Google, offer data
   for payment / backend SWE in the US 2025–2026 (levels.fyi), RSU structure and buyback, negotiation norms.
5. **What the team likely values** in a candidate with Chi's background (inferred from postings and talks; label it).
Output file: `payment_company.md`.

## Output format

Markdown, sections as listed in your task, each claim with a source (URL or id + date) and a confidence
(high / medium / low). End with "## Gaps" (what you could not find or verify). ≤ 3500 words.

## Reply (≤ 10 lines)

What you found that changes how Chi should prepare, the biggest gaps, and anything that contradicts the old catalogue.

# Writer — TikTok / ByteDance kit, retargeted to Global Payment ({PART})

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Write only the files listed in
your part, under `vault/interviews/companies/tiktok/`. These are **learning pages**: follow
`proposals/WRITING_RULES.md` strictly — Chinese prose with English terms in full-width parentheses; **no sources,
report ids, counts of reports, confidence labels, dates of reports, "reconstructed", "面经", "据报告" or process talk**
anywhere (the plain-style checker rejects them); phone-safe diagrams (rule 12); wikilinks only to files that exist.
Textbook tone, senior bar, every term explained where it first appears; concise and self-contained.

## The target (changed)

Chi now interviews for **ByteDance (the employer is ByteDance Inc., not TikTok proper) "Software Engineer, Financial
Product and Solution — Global Payment"** in the US (San Jose / Seattle area), first technical round on Monday,
2:00 PM PT. The old kit targeted "Senior Backend SWE — Innovative Growth" at TikTok; every page must be re-aimed.
Chi: PayPal backend (fee calculation, settlement pipelines, interchange data, on-call), Python / Java / SQL, about two
years full-time; prepare to the **senior (2-2) bar** and ask for a 2-2 loop with a design round.

## Facts (research area; read, do not copy their sourcing)

`research/companies/tiktok/catalog/payment_company.md` (company, org, role, levels, pay, culture) and
`payment_loop.md` (the loop, AI-assisted coding round, class design, fundamentals, pass / fail reasons, payment
prompts), plus the older `company.md`, `loop.md`, `behavioral.md`, `system_design.md`, `CATALOG.md` §2–5.
Chi's stories: `vault/interviews/core/stories/`, `vault/interviews/companies/headlands/behavioral/stories/`.

## Models to copy in shape

`vault/interviews/companies/headlands/` (`README.md`, `00-last-day-roadmap.md`, `01-company-brief.md`, `fit.md`,
`06-questions-to-ask.md`, `behavioral/`) and `vault/interviews/companies/amazon/` (`README.md`, `LOOP_GUIDE.md`).
Existing study material to link to (do not rewrite): Anki decks `LeetCode Tops::24 TikTok 字节高频 · 整题答案`
(tier A sub-deck `01 A 档：最高频`), `::26 工具里的数据结构与算法` (branch `12 数据结构组合` for class design), `支付系统核心`;
Obsidian `[[tiktok-sd-index]]` (SD01–SD12), `[[tiktok-fundamentals]]`, `vault/domains/payments/`.

{TASK}

## Gate

`uv run python scripts/plain_style.py <your files>` ok · `uv run python scripts/phone_diagrams.py <your files>` ok ·
`uv run python scripts/check_wikilinks.py` 0 dead links · `git checkout uv.lock` if changed.

## Reply (≤ 8 lines)

Files written, what changed versus the old pages, anything in the research you left out and why.

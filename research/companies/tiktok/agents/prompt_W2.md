# Writer — TikTok / ByteDance kit, retargeted to Global Payment (W2)

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

## Your part: the loop, behaviour, payment domain, class design

1. `LOOP_GUIDE.md` — rewrite, shaped like Amazon `LOOP_GUIDE.md`: round by round (recruiter, technical rounds with
   resume deep dive + coding on HackerRank / Lark with self-written tests, backend fundamentals, payment system design,
   class design, AI-assisted coding round, HM, HR), for each: what happens, what is scored, how people fail, how to
   prepare, and the time budget inside the hour. Include levelling: how 2-1 vs 2-2 is decided and how to ask for a
   design round.
2. `behavioral/question_bank.md` and `behavioral/deep_dive.md` — update for Global Payment: payment-domain resume
   drill questions (fee calculation correctness, settlement idempotency, reconciliation breaks, on-call incidents,
   money correctness under retries), each mapped to Chi's stories; keep existing good content.
3. `05-payment-domain.md` — new: the payment knowledge an interviewer on this team expects, as a study page:
   money flows (pay-in / pay-out, authorisation / capture / settlement), ledger and double entry, idempotency keys,
   reconciliation, refunds and chargebacks, FX and rounding, plus the consumer-finance layer (PayLater, instalments,
   interest accrual, credit checks); each topic a few paragraphs from zero with a link to the deeper page or deck.
4. `07-class-design.md` — new: payment-flavoured class-design practice (fee / tax calculator with rules, ledger with
   double entry, idempotent transfer service, instalment schedule generator, rate limiter per merchant): for each the
   spec, the data structures and why, the invariants, a minimal Python skeleton (≤ 40 lines, type hints), the follow-ups;
   link the `组合模式` cards in deck 26 and the matching design problems in deck 24.
Delete nothing; if an old page no longer fits, say so in your reply.

## Gate

`uv run python scripts/plain_style.py <your files>` ok · `uv run python scripts/phone_diagrams.py <your files>` ok ·
`uv run python scripts/check_wikilinks.py` 0 dead links · `git checkout uv.lock` if changed.

## Reply (≤ 8 lines)

Files written, what changed versus the old pages, anything in the research you left out and why.

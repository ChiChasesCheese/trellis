# Task — TikTok / ByteDance kit pages (learning area), group K1: company, loop, behavioural

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Write only under
`vault/interviews/companies/tiktok/`. These are **learning pages**: follow `proposals/WRITING_RULES.md` strictly — no
sources, report ids, counts of reports, confidence, dates of reports, "reconstructed", or process talk anywhere; Chinese
prose with English terms; phone-safe diagrams (rule 12). Model the shape on `vault/interviews/companies/amazon/`
(README, LOOP_GUIDE, lp/) and `vault/interviews/companies/headlands/` (01-company-brief, fit, behavioral/, 06-questions-to-ask).

Inputs (research area, for facts only): `research/companies/tiktok/catalog/` (`loop.md`, `coding.md`,
`system_design.md`, `behavioral.md`, `company.md`, `CATALOG.md` §3–4) and Chi's stories:
`vault/interviews/core/stories/` and `vault/interviews/companies/headlands/behavioral/stories/`.

Target: Chi, backend engineer (PayPal payments / fee pipelines, Python / Java / SQL), aiming at TikTok **Senior Backend
Software Engineer** (US). Prepare to the senior bar.

Write:
1. `README.md` — 从这里开始: 3–5 sentences on what the loop is; **先记住几件事** (the 4–6 facts that change how to
   prepare: no OA for experienced hires, resume drill eats the first part of every hour, code must run and you write
   tests, coding mostly medium with follow-ups, payment-style design is the most likely prompt, HM decides level);
   **每天练什么、在哪练** table: coding → Anki `LeetCode Tops::24 TikTok 字节高频 · 整题答案` (read first; start with
   branches 模式识别 and Python 工具箱) then `::25 … · 拆分背诵`; system design → `[[tiktok-sd-index]]`; fundamentals
   (八股) → `[[tiktok-fundamentals]]` (another agent writes it); behavioural → `behavioral/`; **流程** (rounds, levels
   2-1 / 2-2, timeline, team matching).
2. `LOOP_GUIDE.md` — per round: format · what is scored · pass line · failure modes · prep actions (rehearsable).
3. `01-company-brief.md` — the business and products, how TikTok / ByteDance engineering works (stack names that are
   public, scale, culture), US context an interviewer may raise; Chinese, textbook tone, cause → effect.
4. `behavioral/` — `00_how_it_works.md` (HM round and project deep dive: what they probe, how to answer, time limits),
   `question_bank.md` (each question family: which of Chi's stories, the 3–4 beats with **bold keywords**, follow-ups
   with one-line cues — outline style, rule 10), `deep_dive.md` (the project deep-dive drill: the 10–15 questions
   interviewers ask about one project — why this tech, scale numbers, trade-offs, what you would change, failure modes —
   answered as outlines for Chi's two strongest projects), `bytestyle.md` (the six official ByteStyle values, each
   mapped to the story that shows it, one line each). Keep 【待补：…】 where only Chi knows the answer.
5. `06-questions-to-ask.md` — questions for each interviewer type, and what each answer tells you.

Gate: `uv run python scripts/plain_style.py <every page>` (`--outline` for `behavioral/question_bank.md`,
`deep_dive.md`, `bytestyle.md`); `uv run python scripts/phone_diagrams.py vault/interviews/companies/tiktok`;
`uv run python scripts/check_wikilinks.py interviews/companies/tiktok` (links to `tiktok-sd-index` and
`tiktok-fundamentals` may be dead until the other agents finish — list them). Reply ≤ 8 lines.

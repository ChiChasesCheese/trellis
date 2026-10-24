# Task — TikTok / ByteDance system design pages, group {GROUP}

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Write only the files named
below in `vault/interviews/core/system-design/tiktok/`. Learning pages: `proposals/WRITING_RULES.md` strictly (no
sources, report counts, confidence or process talk; Chinese prose with English terms; diagrams within rules 9 and 12).

Copy the shape and depth of `vault/interviews/core/system-design/amazon/sd01-url-shortener.md` exactly: 题目 (what it
is, why it is hard, what the interviewer says) · 澄清问题 (each with why it changes the design) · 需求 (functional by
priority; non-functional table) · 估算 (numbers computed, shown) · API · 数据模型 · 高层设计 (diagram + numbered
flow) · 深挖 (3–5 deep dives, each a decision with alternatives and the reason) · 故障与边界 · 追问 (8–12 follow-ups
with answers) · 评分要点 (what a senior answer must hit). Senior bar. Every number re-derived with `python3 -c`.

Facts about what TikTok interviewers push on: `research/companies/tiktok/catalog/system_design.md` and `CATALOG.md` §2
(read the "What interviewers pushed on" column; make those the deep dives and follow-ups).

Your files: {FILES}

Gate: `uv run python scripts/plain_style.py <files>`; `uv run python scripts/phone_diagrams.py <files>`;
`uv run python scripts/check_mermaid.py <files>` if it exists. Reply ≤ 8 lines with files, gate results and the numbers
you are least sure of.

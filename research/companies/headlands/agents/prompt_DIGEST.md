# Task — Headlands "18 题速读" (solutions digest), one page

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents. Write only
`vault/interviews/companies/headlands/08-solutions-digest.md`.

Chi has one day left before the Headlands technical video interview (CoderPad, Java or C++ at the interviewer's
choice). He will **read along with the answers** instead of writing every problem: the page must make each problem's
answer and principle clear in one screen, so he can understand and explain it. Tutorial tone, Chinese with English
terms, concise, skimmable. Learning-page rules: `proposals/WRITING_RULES.md` (no provenance, no process talk).

Problems (in this order — most likely first): hc05 market order book, hc14 VWAP trade log, hc15 streaming median,
hc16 tree DP, hc07 ticker hash map, hc02 merge k streams, hc04 queue mean snapshot, hc09 top trades by notional,
oa01 job chain, hc01 stock trading DP, hc03 recursive sum, hc08 order sequence API, hc11 order interval overlap,
hc06 CPU register bitwise, hc13 fixed memory pool, ld01 SPSC channel, ld02 trading OOD, ld03 async TCP channel.
Sources for each: `loop/rounds/<round>/<id>/problem.md`, `reference/*.java`, `cpp/reference.hpp`, and
`study/30-articles/<id>.md` + `<id>_cpp.md` (all under `vault/interviews/companies/headlands/`).

Page shape:
- 3-line intro: how to use the page (read top to bottom; each entry ~5 minutes; open the article only when stuck).
- A table of contents: one row per problem — `[[#…]]` anchor link, one-line essence, difficulty feel.
- One `## <id> · <title>` section per problem, **≤ 30 lines**, exactly these bold labels as bullets:
  **题意**（一两句 + 最小例子） · **核心思路**（2–4 句，讲清为什么这样做） · **数据结构**（选什么、为什么、复杂度） ·
  **Java 要点**（地道写法 2–3 条，类名与 API） · **C++ 要点**（和 Java 不同的地方 2–3 条：容器对应、所有权、溢出、
  迭代器失效） · **易错点**（2–3 条，具体） · **追问**（2–3 条，每条一句答案） · **链接**（`[[<id>|Java 讲义]]` ·
  `[[<id>_cpp|C++ 讲义]]`）.
- Short code only where it is the heart of the answer (≤ 12 lines, Java), taken from the reference.

Gate: `uv run python scripts/plain_style.py vault/interviews/companies/headlands/08-solutions-digest.md`,
`uv run python scripts/phone_diagrams.py` on it, `uv run python scripts/check_wikilinks.py interviews/companies/headlands`
(0 dead links); `git checkout uv.lock`. Reply ≤ 5 lines.

# Writing rules for learning pages (Chi, 2026-10-16 / 10-17)

Chi: 「出处就完全不要提到；你要留档用你自己的 log，不要展现在 Obsidian 用来学习/背诵的文章中。尽量让所有文章都变成
能用来背/学习的 action item。打开 Obsidian 直接进入主题，不被展示任何 discovery / preparation 过程的信息，只看关键信息。」

A **learning page** is anything under `vault/` a learner reads: articles, solution write-ups, drills, study notes, LP
outlines, indexes, and every card. Process material (sources, evidence, agent instructions, ledgers, checkpoints, gates,
scripts) lives outside the vault, in `research/companies/<co>/` or `proposals/`. Machine-checkable rules are enforced by
`scripts/plain_style.py`, called from `scripts/check_sd.py` and `scripts/check_lld_problems.py --branch amazon`.

1. **No provenance, no process — anywhere.** Never say where or when a question was reported, by whom, on which site,
   with what confidence, or that a part was reconstructed / inferred; no thread ids, report dates, post URLs, commit
   hashes, evidence tables, paths of agent instructions, "verified by", "gate", "ledger". If provenance is worth
   keeping, append it to `research/companies/<co>/PROVENANCE.md`. The page states the problem as the problem.
   Study links (docs, a tutorial page, a related note) are fine, only in a final `## 延伸阅读` section.
2. **Every page is something to study or rehearse.** Lead with what to know / say / do. Cut anything that is not a fact,
   a decision with its reason, a step, a question to practise, or an answer to rehearse. No meta-commentary about the page.
3. **Talk to the reader, not about the text.** Plain exposition, or 「你」 for instructions. Never 本篇 / 本文 / 本题 /
   这道题 / 作者 / 我们认为 / 候选人说.
4. **Cause → effect.** Each design choice: what forces it and what it buys and costs.
5. **Plain words, terms defined on first use** — one plain line, then the English name in full-width parentheses.
6. **Self-contained.** The page can be understood alone; links are further reading.
7. **Open with the topic in plain words** (3–5 sentences) before any list or table.
8. **Priority label.** A problem not asked within the last month carries `（low priority）` at the end of its title (H1 and
   index row). No explanation of why — the label is enough.
9. **Diagrams that fit a page** (Obsidian column ≈ 700 px):
   - `flowchart TB` / `graph TD` only; ≤ 12 nodes; ≤ 4 side by side; labels ≤ 16 characters; split write path / read path.
   - `sequenceDiagram`: start with `%%{init: {'sequence': {'actorMargin': 16, 'width': 104, 'messageMargin': 28}}}%%`,
     `autonumber`, ≤ 5 participants, every message ≤ 24 display units (a CJK character counts 2); explain each numbered
     step in a list under the diagram.
   - `classDiagram` ≤ 8 classes, one member per line, ≤ 3 classes hanging off one class.
10. **LP / behavioural pages are outlines only.** Bullet lists, no paragraphs. For each story: one-line headline, then
    S / T / A / R / L bullets with **bold keywords** to say aloud, numbers inline. For each question: the answer framework
    (which story, the 3–4 beats to hit), 2–4 follow-up questions an interviewer asks next, each with a one-line answer
    cue. An LP ↔ story mapping table is part of the set. Nothing else — no explanation of why LPs matter, no process.
    Placeholders Chi must fill stay as 【待补：…】 bullets (they are action items).
11. **Cards.** Front asks something answerable from understanding; no provenance anywhere on the card, including the
    footer (the footer only links the study note in Obsidian). A meta chip says at most difficulty and a priority label.
12. **Diagrams must survive a phone** (Chi, 2026-10-22: wrapped ASCII art was unreadable in Obsidian on iPhone).
    A text diagram in a fenced block is at most **40 display columns** (CJK counts 2) and has **no CJK characters on a
    line that draws** (CJK glyphs are not exactly two cells wide, so box edges drift) — put labels in a legend list or
    table under the diagram. Prefer, in order: a table, a short numbered list, a mermaid diagram within rule 9's limits,
    and only then narrow ASCII. Checked by `scripts/phone_diagrams.py`. Program output blocks are not diagrams; the
    vault's `no-wrap-code` CSS snippet makes them scroll sideways instead of wrapping.


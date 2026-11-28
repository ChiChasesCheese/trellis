# Task: give Markets and Quant Infrastructure's Anki-only cards a home in the vault, in Chinese

Chi (2026-11-28): every card has one source, in git; Markets & Factors and Quant Infrastructure are kept and shown on
the Atlas, and he will study them in Chinese. Today `skeleton/markets.yaml` and `skeleton/quant-infra.yaml` (English,
`lang: en`) have readings but **no card files**, while Anki holds 46 (`📦 其他::Markets & Factors`) and 86
(`📦 其他::Quant Infrastructure`) notes, plus some of them borrowed into `6 Millennium`. Most carry no `id::` tag; 37
carry `id::anki-<note id>` (adopted mirrors whose files are gone); their `<domain>::<node path>` tags say which leaf.

Read first: `AGENTS.md`, `CONTEXT.md` (Adopted card), `trellis/adopt.py` (how a deck that lives only in Anki becomes
a domain: `trellis adopt --anki`), `docs/translation-spec.md` (`## Q zh` / `## A zh` sections, `show: zh`), five
`vault/interviews/rounds/code-core/cards/` files (an English domain shown in Chinese — the precedent),
`trellis/build.py` `NOTE_FIELDS` (never write `Note` / `NoteAnswer`).

## Do

1. Inventory every note in both decks and every note in any deck tagged `markets::*` or `quant-infra::*`: note id,
   model, `id::` tag if any, domain/node tag, which skeleton leaf it maps to (node tag → leaf id; say when none fits).
2. Write one vault card per note under `vault/domains/markets/cards/` and `vault/domains/quant-infra/cards/` (check the
   skeletons' `vault:`), in the trellis card format: `id` (keep an existing `anki-<nid>` id; otherwise a readable
   slug id), `node`, `type`, and the note's own question/answer (or cloze text) as the English body, plus a faithful
   `## Q zh` / `## A zh` (or cloze zh) translation following the spec. Set `show: zh` in both skeletons.
   Card by card. Fix obvious English errors and list them.
3. Prefer `trellis adopt --anki` if it does this correctly; otherwise write the files directly. Either way, the Anki
   notes must end up tagged `id::<card id>` so traces map: list the (note id, id tag) pairs you need added in
   `sources/local/audit/markets-quant-adopt.json` and DO NOT write to Anki yourself — the orchestrator adds the tags.
4. `uv run trellis --domain markets validate` and `--domain quant-infra validate` 0 errors; pytest green.

Do not commit, push, or touch Anki (read-only queries only). Do not spawn agents. Other agents are working on
LeetCode sources and on the system-design migration; stay in these two domains. Report: notes found, cards written per
domain, notes that fit no leaf, English errors fixed, and the five translations you are least sure about.
Resume rule: skip notes whose card file exists.

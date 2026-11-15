# Changelog

## Trellis 1.0 — the study system (2026-11-15)

The engine's v1.x tags cover building and pushing decks. 1.0 is the system built on top of it. It decides what Chi
studies each day, keeps one source for every piece of content, and preps a whole interview loop end to end. The
overview is in `docs/explanation/study-system.md`.

- **One card per LeetCode problem.**
  - 819 bodies, each with exactly one card on the 0x3F knowledge tree. Our own leaves cover what his lists miss.
  - Lists, companies, 已做过 and 必读 are tags (`lc_tags.py`); views are built by `lc_view.py`.
  - The copy decks are gone. LeetCode Tops became **Under the Hood**: algorithm material that is not a problem.
- **Design questions as the target** (`deep_dive.py`). One question a day, with:
  - its foundations (every exam point it needs, prerequisites first);
  - mock-interview fixes (`mock_fix.py`);
  - 完整答案 with a diagram on every card, written ahead each day for the next question.
- **Interview sprints.**
  - Role tracks (`tracks/`: AI-infra SDET, inference infra, inference deployment) plus a company overlay.
  - The overlay is borrowed into a sprint deck (`company_deck.py`, several decks, `rename`, `release`).
  - Plan order is enforced with `reposition_new.py`. Track maps come from `knowledge_tree.py --track`.
- **New domains:** test-release, llm-inference (from zero), ml-system-design, plus the Cerebras kit and deck.
- **Pictures.**
  - A ≥25% diagram floor (`diagram_share.py`), with backfill each night (`diagram_queue.py`).
  - Bare `<svg>` blocks render in Obsidian and Anki alike.
- **Chinese everywhere.** English-source decks with translations set `show: zh`. AI material starts from zero.
- **Card notes live.** Note / NoteAnswer on every note type; questions typed on the phone are answered nightly.
- **Privacy.** Public by default; NDA material and employer internals stay local.

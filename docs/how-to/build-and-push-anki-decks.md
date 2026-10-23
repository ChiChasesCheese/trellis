# How to build and push Anki decks

Prerequisites: `uv`, desktop Anki running with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on
(`:8765`), logged in to AnkiWeb. Only `build` works without Anki. Behaviour and rationale: ADR 0010 and the README
sections "Publishing to the phone" and "The order and the mix Anki deals".

## The routine

```bash
uv run trellis --all validate                 # 0 errors is the bar
uv run trellis --all sync                     # regenerate Obsidian map notes
uv run trellis --all build                    # dist/<domain>.apkg (no --lang: a Chinese-native domain aborts --lang zh)
uv run trellis --domain system-design anki-push --lang zh   # one domain, one language
uv run trellis --all anki-push                # every domain
```

`anki-push` builds the package itself, then: syncs AnkiWeb (phone reviews land first) -> imports -> aligns decks and card
positions to the skeleton -> syncs again. Switching `--lang` rewrites card text in place; review history survives.

## Review loop (read-only against Anki)

```bash
uv run trellis --all pull          # review history -> traces/<domain>.json
uv run trellis --all brief         # vault/Brief.md: what to do next
uv run trellis --domain <d> anki-align    # converge decks / positions without importing
```

## When it goes wrong

- **'Collection lifecycle operation is active'**: the push imported while AnkiWeb sync was still running. Sync, wait until
  AnkiConnect answers, `importPackage`, then `trellis --domain <d> anki-align`.
- **New cards in the wrong order**: AnkiConnect refuses to write `due` on cards. For still-new, never-reviewed cards:
  `deleteNotes`, then re-import the `.apkg`; positions follow the package's Sequence order.
- **A domain is missing in Anki**: a domain with 0 cards builds no deck.
- **Review limit hides new cards**: enable *Deck options -> New cards ignore review limit* (collection-wide, one checkbox).
- **Tests and Anki**: a test touching Anki must replace `cli._anki_call` with a fake (`tests/test_loop_e2e.py`); never point
  a test at the live collection.
- Never write to the shared `Default` preset or to a reviewed card's `due`. Domains get their own `Trellis · <title>` preset.
- Company kits are not trellis domains; syncing adds no cards for them. Amazon coding cards go in through
  `scripts/amazon_push_cards.py` (see its docstring).

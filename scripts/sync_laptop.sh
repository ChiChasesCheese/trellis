#!/usr/bin/env bash
# Pull the latest main and bring this machine's Obsidian vault + Anki up to date.
#
#   bash scripts/sync_laptop.sh            # pull main, validate, sync map notes, build decks, push to Anki if it is running
#   bash scripts/sync_laptop.sh --no-anki  # everything except the Anki step
#
# First-time setup on a new laptop (once):
#   git clone https://github.com/ChiChasesCheese/trellis.git ~/Code/trellis
#   curl -LsSf https://astral.sh/uv/install.sh | sh          # uv, if missing
#   open Obsidian -> "Open folder as vault" -> ~/Code/trellis/vault   (the whole vault/, not one domain)
#   install desktop Anki + the AnkiConnect add-on (code 2055492159), keep Anki open while syncing
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
NO_ANKI=0
[[ "${1:-}" == "--no-anki" ]] && NO_ANKI=1

echo "== 1/5 git: pull main"
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "   local changes found; stashing them (git stash list to see them)"
  git stash push -u -m "sync_laptop $(date +%F-%H%M)"
fi
git checkout main
git pull --ff-only origin main

echo "== 2/5 uv: dependencies"
command -v uv >/dev/null || { echo "uv not found: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
uv sync --quiet

echo "== 3/5 trellis: validate (0 errors is the bar)"
uv run trellis --all validate

echo "== 4/5 trellis: sync map notes + build decks"
uv run trellis --all sync
uv run trellis --all build          # no --lang: Chinese-native domains abort under --lang zh

echo "== 5/5 anki"
if [[ $NO_ANKI -eq 1 ]]; then
  echo "   skipped (--no-anki)"
elif curl -s -m 2 -X POST localhost:8765 -d '{"action":"version","version":6}' >/dev/null 2>&1; then
  uv run trellis --all anki-push     # pulls AnkiWeb first, imports, aligns decks, pushes AnkiWeb
else
  echo "   desktop Anki (AnkiConnect on :8765) is not running; decks are in dist/*.apkg — open Anki and rerun, or import them by hand"
fi

echo
echo "done. Obsidian: open $ROOT/vault as the vault. Millennium kit: vault/interviews/companies/millennium/00-README.md"
echo "      practice: cd vault/interviews/companies/millennium && python3 loop/mock.py start pc02 -m 30"

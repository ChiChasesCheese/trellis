# Repo checks, the same ones CI runs. `just` lists the recipes. Details: docs/reference/checks.md.
export UV_FROZEN := "1"
set shell := ["bash", "-euo", "pipefail", "-c"]

[private]
default:
    @just --list

# trellis package: validate every skeleton, run tests/, no dead wikilinks
test:
    uv run trellis --all validate
    uv run --with pytest python -m pytest -q
    python3 -B scripts/check_wikilinks.py

# every interview kit's practice suites (about 4 minutes; `just kits stripe` for one; needs mvn, JDK 21, a C++ compiler for headlands)
kits co="":
    python3 -B scripts/kit_suites.py {{ if co == "" { "" } else { "--co " + co } }}

# style checks on the learning pages changed since BASE (default: the working tree vs HEAD)
style base="":
    python3 -B scripts/changed_learning_pages.py {{ if base == "" { "" } else { "--base " + base } }} --check

# mermaid diagrams on the changed pages must render (needs Node)
mermaid base="":
    python3 -B scripts/check_mermaid.py {{ if base == "" { "" } else { "--base " + base } }}

# everything above
all: test kits style

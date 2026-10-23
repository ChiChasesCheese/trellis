# How to add a company kit

A kit is the interview preparation for one company. It is split in two areas (ADR 0011): the **learning area**
`vault/interviews/companies/<co>/` that Chi studies, and the **research area** `research/companies/<co>/` that records how
it was made. Full procedure and red flags: `.claude/skills/building-company-interview-kits/SKILL.md`. Agent rules:
`AGENTS.md`, "Interview kit methodology".

## Steps

1. **Create both folders.** `vault/interviews/companies/<co>/` (lower-case company slug) and `research/companies/<co>/`.
2. **Search GitHub first**, then forums and aggregators. Write one file per source into `research/companies/<co>/catalog/raw/`
   (every fact with URL and date, nothing rewritten). LeetCode originals get no full kit: run
   `python3 vault/interviews/core/leetcode/lc_company.py <Company>` and map ids in `core/leetcode/companies/<co>.kitmap.json`.
3. **Rank.** `catalog/CATALOG.md`: one row per problem (aliases, stage, parts, last asked, `#refs`, confidence, URLs). The top
   ~20% of rows should cover ~80% of sightings; write the cut line down. Counts come from a script, not from memory.
4. **Write `research/companies/<co>/README.md`** (5-10 lines: what is here, where the learning pages are), then
   `CHECKPOINT.md`, `LEDGER.md`, `PROVENANCE.md` as work proceeds. Task files for agents are `<NAME>_TASK.md` here.
5. **Write the learning pages** in `vault/interviews/companies/<co>/`:
   - `README.md` is the only entry point.
   - Keep only company-specific rounds and topics here: `LOOP_GUIDE.md`, LP outlines, company-only rounds.
   - General topics (system design, coding, LLD) go to `vault/interviews/core/<topic>/<co>/` or to a domain branch.
   - Learner-facing text is Chinese, technical terms in English in parentheses.
   - Practice material (problem dirs with tests, `drill.py`, `loop/mock.py`) stays in the kit; builders and rankers do not.
6. **Apply the writing rules** (`proposals/WRITING_RULES.md`): no provenance, no process talk, `（low priority）` on problems
   not asked in the last month, diagrams that fit a phone. Provenance goes to `PROVENANCE.md`, never to a learning page.
7. **Name new things per ADR 0012** (`README.md` entry, `00_` prefixes, `<prefix><nn>_<snake_slug>` problem dirs).
8. **Optional deck.** A trellis domain for the company lives in `deck/` with `skeleton/<co>.yaml` setting
   `vault: interviews/companies/<co>/deck` (ADR 0008). Kits themselves are not domains.

## Checks before you stop

```bash
python3 scripts/plain_style.py <pages>            # LP pages: --outline
python3 scripts/phone_diagrams.py vault/interviews/companies/<co>
python3 -B scripts/check_wikilinks.py | tail -1   # 0 dead link(s)
cd vault/interviews/companies/<co> && python3 -m pytest problems -q   # the kit's own suite, if it has one
```

## Migrating an old kit

An older kit with sources, ledgers and tools inside `vault/` is split with `git mv` following
`research/agents/MIGRATE_KIT_TASK.md`. Run the practice suites before and after and compare pass counts.

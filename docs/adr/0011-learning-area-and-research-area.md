# The vault is the learning area; how it was made lives in the research area

Date: 2026-10-17 (decided), 2026-10-23 (kit migrations done).

Company kits grew inside `vault/interviews/companies/<co>/` with everything that produced them: raw sources, catalogs,
confidence columns, ledgers, checkpoints, agent rules, harvest JSON and authoring tools. Chi opens that folder in Obsidian to
study, and on the phone the evidence tables, report ids, "reconstructed" labels and gate talk sat between him and the
material. Chi (2026-10-17): provenance is never shown in Obsidian; keep your own log elsewhere; make every page something to
learn or rehearse. Amazon was the first kit written that way, Headlands the second.

We now keep two areas:

| Area | Path | Contents |
|---|---|---|
| Learning | `vault/` | only what Chi studies or practises with: entry `README.md`, guides, LP outlines, study articles, problem dirs with their tests, the minimum runner (`drill.py`, `loop/mock.py`, `conftest.py`, `pytest.ini`) |
| Research | `research/companies/<co>/` | sources and evidence (`catalog/`, `reports/`, harvest JSON), process (`CHECKPOINT.md`, `LEDGER.md`, `HANDOFF.md`, `CONVENTIONS.md`, `PROVENANCE.md`, `*_TASK.md`, agent rules), authoring tools, card JSON |
| Research, cross-cutting | `research/agents/` | task files not tied to one company |

Inside the vault, `companies/<co>/` keeps only company-specific rounds and topics. A general topic prepared for one company
goes to `vault/interviews/core/<topic>/<co>/` or to a domain branch. Provenance a page would have cited goes to
`PROVENANCE.md`. The page rules are `proposals/WRITING_RULES.md`; `scripts/plain_style.py` enforces the machine-checkable
half, `scripts/check_wikilinks.py` guards links. `research/AGENTS.md` describes the research side for agents.

**Consequences.** A kit is migrated with `git mv` only (`research/agents/MIGRATE_KIT_TASK.md`), so history follows the files;
relative links and tool paths need re-pointing, and some moved tools still assume they run from the kit root. Practice suites
must give identical pass counts before and after. On 2026-10-23 the kits for Snowflake, Stripe (244 files moved; problems 1086
pass, loop 866/82, unchanged), Airbnb (81), Roblox (37), Millennium (263 passed, 1 skipped) and Abnormal (per-suite outputs identical)
were split this way. Style debt in older learning pages (provenance, process talk) is a separate cleanup, not part of a
migration. `snowflake/`, `millennium/` and `abnormal/` keep a `CONTENTS.md` index next to their `README.md`; its practice runner stays in the kit.
Authors of new kits follow `docs/how-to/add-a-company-kit.md`.

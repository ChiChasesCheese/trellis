# Docs

Contributor and agent documentation, in four kinds (Diataxis). Study material for Chi is in `vault/`, not here. Product
overview: [../README.md](../README.md). Agent rules and repository map: [../AGENTS.md](../AGENTS.md). Vocabulary:
[../CONTEXT.md](../CONTEXT.md).

## How-to (a task to get done)

- [Add a company kit](how-to/add-a-company-kit.md)
- [Build and push Anki decks](how-to/build-and-push-anki-decks.md)
- [Obsidian and sync setup](how-to/obsidian-sync.md)

## Reference (facts to look up)

- [Checks](reference/checks.md): every checker script, how to run it, exit codes
- [CLI](reference/cli.md): `trellis` commands and options
- [Translating cards](translation-spec.md)
- [Writing rules for learning pages](../proposals/WRITING_RULES.md)

## Explanation (why it is built this way)

- [Architecture](explanation/architecture.md): skeleton to cards to Anki, vault vs research, sync

## Decisions (ADRs)

| # | Decision |
|---|---|
| [0001](adr/0001-obsidian-as-the-reader.md) | Obsidian is the reading surface; Anki links into it |
| [0002](adr/0002-skeletons-are-authored-from-the-field.md) | Skeletons are authored from the field |
| [0003](adr/0003-a-codebase-enters-as-cases-and-subject-material.md) | A codebase enters as cases and subject material |
| [0004](adr/0004-traces-are-pulled-into-a-file-the-repo-owns.md) | Traces are pulled into a file the repo owns |
| [0005](adr/0005-a-leaf-is-sealed-until-its-prerequisites-hold.md) | A leaf is sealed until its prerequisites hold |
| [0006](adr/0006-a-corpus-enters-as-readings-and-may-seed-a-skeleton.md) | A corpus enters as readings and may seed a skeleton |
| [0007](adr/0007-adopted-notes-stay-with-their-owner-and-the-workbench-is-local.md) | Adopted notes stay with their owner; the Workbench is local |
| [0008](adr/0008-the-vault-is-organised-by-purpose-and-a-skeleton-places-its-domain.md) | The vault is organised by purpose; a skeleton places its domain |
| [0009](adr/0009-the-loop-waits-for-a-verdict-before-it-acts-again.md) | The loop waits for a verdict before it acts again |
| [0010](adr/0010-the-vault-decides-the-order-and-the-mix-anki-deals.md) | The vault decides the order and the mix Anki deals |
| [0011](adr/0011-learning-area-and-research-area.md) | Learning area and research area |
| [0012](adr/0012-naming-and-layout-for-new-content.md) | Naming and layout for new content |

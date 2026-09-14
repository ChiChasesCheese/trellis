# The vault is organised by purpose, and a skeleton places its domain

The vault had grown to fifteen top-level folders: eleven domains, the interview
folder, a Stripe domain whose problem write-ups duplicated the Stripe kit, and two
generated indexes. A reader looking for "everything about interviews" had to know
that `code-core`, `leetcode`, `narrative` and `stripe` were interview material
living beside `kafka` and `basketball`, and the kits could not point at the coding
round's general leaves without a reader already knowing the domain existed.

We now organise the vault by purpose, two levels deep:

```
vault/
  domains/<subject>/                   what is worth knowing (system-design, kafka, snowflake …)
  interviews/core/                     company-agnostic interview material (resume, stories, answers)
  interviews/rounds/<round-domain>/    the transferable round skills (code-core, leetcode, narrative)
  interviews/companies/<co>/           one self-contained kit per company; a company deck lives in deck/
  Brief.md, Codebases/, Corpora/       generated indexes
```

A skeleton says where its content lives with `vault: <relative path>`; without
it the folder is the domain slug, so older checkouts keep working. The slug stays
the domain's identity everywhere else: card ids, Anki deck names and GUIDs, traces
and the `--domain` flag never mention the folder, so moving a domain is a
`git mv` plus one skeleton line.

Links do not depend on the move. Cards, drills and map notes link by note name,
and note names are unique across the vault, so Obsidian resolves them from any
folder. What the move buys is cohesion: every interview-facing note sits under one
folder, and the company kits link to the round skills they rely on through the
code-core `transfer.<company>` leaves and each round's `core:` list.

**Consequences.** `trellis adopt` still scans only the top level of `vault/` for
folders without a skeleton; a hand-built folder has to sit at the top level to be
discovered, and is moved into place after adoption. A company deck and its kit
share a folder: the kit is plain notes, the deck is the trellis domain in `deck/`,
and a problem is written once in the kit and linked from the deck.

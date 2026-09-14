---
nodes:
- storage.record-modeling
title: One honest ledger with a discriminator, not two stores
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0001-strategy-stack-not-layer
---

# One honest ledger with a discriminator, not two stores

Two kinds of thing keep getting conflated in reports, so the tempting fix is to split them into separate stores. Splitting is usually the wrong move: it destroys any accounting that must span both kinds, and it doubles every piece of tooling that touches either. The alternative is to keep one store and add a dimension that discriminates them, letting the presentation layer group by it. You pay with a wider record and a column that is meaningless for some rows; you keep the ability to ask questions across the whole population — which is exactly the kind of question that motivated the split in the first place.

The second half of the lesson is naming, and it is the half that bites. The obvious name for the new dimension was already the canonical word for an unrelated axis in the same system. One word carrying two meanings was not a cosmetic problem — it was the root cause of the misreading that triggered the change. A schema is a vocabulary before it is a layout, so a term collision is a design defect with the same standing as a missing index, and it should be resolved before the migration rather than after.

---
nodes:
- analytics.derived
title: Materialize the archive, derive the rest
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0002-data-stages-raw-bars-panel-not-lake-layers
---

# Materialize the archive, derive the rest

A data pipeline usually has three stages: an immutable archive of what a source actually sent, a canonical per-entity series, and an aligned cross-entity view for analysis. The design question is which of these are bytes on disk and which are computed on read.

Materializing only the archive means cleaning rules can change without a migration, there is never a reconciliation problem between stages, and every derived table can be rebuilt from the record; the price is recomputation on every read, plus the *option* — not the obligation — to materialize later when that cost bites.

Normalization belongs in a per-source adapter at the boundary between archive and canonical series: the archive is partitioned by source, each source brings its own quirks and its own adapter, and everything above the boundary is source-agnostic. Adding a source is then one partition plus one adapter. The tell that you got this wrong is a source that reaches analysis by its own private path, so every downstream consumer grows a special case.

Naming is not cosmetic here. Borrowed jargon that misdescribes the physical reality (calling a single-source archive a "lake") and numbered layers that collide with another axis in the same system both cost every future reader time; nouns already present in your own API are free.

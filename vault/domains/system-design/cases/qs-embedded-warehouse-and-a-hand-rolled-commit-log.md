---
nodes:
- analytics.warehouse
- analytics.batch
title: An embedded warehouse and a hand-rolled commit log
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0003-embedded-data-platform-duckdb-dbt-sealed-snapshots
---

# An embedded warehouse and a hand-rolled commit log

The modern-data-stack shape — warehouse, declarative transforms, orchestrator, table format — can be had at small scale without running a single server.

An embedded analytical engine that queries files in place gives SQL and columnar scans with no daemon to operate, and the same engine in tests as in production, so "tested against a real database" costs a temp file rather than a container. Transforms move from imperative read-time code into a declarative SQL DAG with per-model schema tests, lineage, and selective rebuild of one subtree.

Orchestration is where teams overspend. A resident scheduler exists for unattended timers and sensor polling; if a human triggers the run, a single command that ingests, validates, rebuilds the affected subtree, tests, and exits is enough. Add the daemon when nobody is watching, not before.

History, rollback and locking come from the commit-log idea in miniature: partitions are append-only and immutable; a batch becomes visible only when a manifest (batch id, row counts, checksums, validation verdict) is written *after* the checks pass; readers see sealed partitions only; rollback moves a CURRENT pointer and derived tables rebuild from the archive. Open table formats formalize exactly this — you can buy most of it by hand and adopt one later.

One operational note: give the transform toolchain its own lockfile, so its dependencies cannot silently bump the main one.

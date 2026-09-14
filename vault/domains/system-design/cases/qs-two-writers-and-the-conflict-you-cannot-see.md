---
nodes:
- distributed.replication.multi-leader
title: Two writers and the conflict you cannot see
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0009-canonical-ledger-outside-worktree-git-mirror
---

# Two writers and the conflict you cannot see

Two lessons about where a system of record lives.

First, never keep it inside a directory that tooling is allowed to rebuild or clean. Records removed by a routine cleanup are indistinguishable from records that never existed, and partial loss of an event log silently corrupts every aggregate that assumes completeness — a correctness bug arriving through storage topology rather than code. Put the source of truth outside the working copy, commit a derived snapshot for consumers that cannot reach it, and label that snapshot a mirror so nobody promotes it to truth. If "which store am I writing to" is a free-form path parameter, make it a type with named constructors and make the conservative reading the default for a bare path.

Second, distrust the sentence "the files are immutable and content-named, so copying can never conflict". Verify it. Here one field was stamped from the destination rather than the record, and a later pass rewrote existing rows — so the premise was false. With it false, a copy tool told to skip existing files is not avoiding conflicts; it is resolving them last-writer-wins by arrival order, dropping a record.

The fix is the multi-leader playbook: compare by content, not bytes (serializers change bytes); classify some differences as provenance rather than conflict; on a real conflict keep both siblings where reader queries cannot see them, alert, and exit non-zero for a human.

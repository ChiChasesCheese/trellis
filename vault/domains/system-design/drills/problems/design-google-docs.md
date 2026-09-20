---
nodes: [problems.media.google-docs, distributed.crdt, networking.realtime]
tags: [problem]
---
# Drill: Design a collaborative document editor like Google Docs

Design the concurrent-editing core of a document editor: several users typing in the same
document at once, seeing each other's cursors, and staying byte-identical after a burst of
concurrent inserts, deletes and formatting changes.

**Constraints to state and honor**
- A document can have up to a few hundred simultaneous editors on rare hot documents; most documents have 1–3.
- Local keystrokes must render instantly (no waiting on a server round trip) while still converging.
- Cursor/presence updates may be dropped or arrive out of order; text operations may never be lost or misordered.
- Version history must support restoring any point in time without the raw operation log growing unbounded forever.

**Grading points**
- Chooses a single authoritative ordering node per document and explains why a document's edits can't be split across multiple ordering nodes the way most keyed data can be sharded ([[problems-google-docs-single-writer-per-document]]).
- Describes the ack-based control loop where a client buffers local operations until the server acknowledges the previous batch, and why this keeps the server's state space to just its own operation history ([[problems-google-docs-server-authoritative-ack-flow]]).
- Explains the interleaving anomaly in rich-text merging and how anchoring formatting spans to stable character identifiers avoids it ([[problems-google-docs-interleaving-anomaly-stable-anchor]]).
- Routes presence/cursor updates through a separate, lossy, unordered channel instead of the durable document operation log, and justifies it by the different cost of a stale cursor vs a stale edit ([[problems-google-docs-presence-separate-channel]]).
- Argues the OT-vs-CRDT trade-off concretely (tombstones and position identifiers vs transform-function correctness burden) rather than naming one algorithm without justification ([[problems-google-docs-ot-vs-crdt-tradeoff]]).
- Computes why storing every raw operation forever costs far more than the documents themselves and designs a snapshot/compaction retention policy instead ([[problems-google-docs-oplog-vs-content-storage-ratio]]).
- Identifies that a single hot document cannot be relieved by sharding and proposes a product-level cap on simultaneous editors ([[problems-google-docs-hot-document-cap]]).
- Recognizes that cross-region multi-master editing would require reconsidering OT for a CRDT-based model, not just adding servers ([[problems-google-docs-cross-region-multimaster-pivot]]).

**Solution**: [[solution-google-docs]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):

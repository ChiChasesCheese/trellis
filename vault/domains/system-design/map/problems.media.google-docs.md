%% trellis:begin %%
# Collaborative Editing (Google Docs)
*Design Problems / Media, Files & Collaboration*

Concurrent edits converging through OT or CRDTs, cursors and presence, and document storage.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/distributed.crdt|CRDTs & Local-First]], [[domains/system-design/map/networking.realtime|Realtime Delivery]]

## Readings
- [[solution-google-docs|设计题解：协同文档编辑（Collaborative Editing / Google Docs）]]
- [[src-apachewave-google-docs|Google Wave Operational Transformation]]
- [[src-bytebytego-google-docs|How to Design Google Docs]]
- [[src-figma-google-docs|How Figma's multiplayer technology works]]
- [[src-googledriveblog-google-docs|What's different about the new Google Docs: Conflict resolution]]
- [[src-inkandswitch-google-docs|Peritext: A CRDT for Collaborative Rich Text Editing]]

## Drills
- [[design-google-docs|Drill: Design a collaborative document editor like Google Docs]]

## Cards (8)
1. [[problems-google-docs-oplog-vs-content-storage-ratio]]
2. [[problems-google-docs-single-writer-per-document]]
3. [[problems-google-docs-ot-vs-crdt-tradeoff]]
4. [[problems-google-docs-server-authoritative-ack-flow]]
5. [[problems-google-docs-interleaving-anomaly-stable-anchor]]
6. [[problems-google-docs-presence-separate-channel]]
7. [[problems-google-docs-hot-document-cap]]
8. [[problems-google-docs-cross-region-multimaster-pivot]]
%% trellis:end %%

## Notes

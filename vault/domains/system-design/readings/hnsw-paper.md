---
nodes: [ai.vector-search]
url: https://arxiv.org/pdf/1603.09320
tags: [canonical, paper]
---
# Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs

Malkov & Yashunin's HNSW paper — the index inside essentially every vector
database (FAISS, Lucene, pgvector, Pinecone, Qdrant). Read sections 3 and 4
for the algorithm and the parameters you will actually be asked about; the
figures make the layered-graph idea land in one look.

**Extract on read:**
- The structure: a hierarchy of proximity graphs, coarse top layer for long hops, dense bottom layer for the fine search — logarithmic hops instead of a linear scan.
- The three knobs and their trade-offs: `M` (graph degree → memory), `efConstruction` (build time → graph quality), `ef` (search breadth → recall vs latency).
- Why it is memory-hungry and deletion-hostile — the practical reasons real systems rebuild segments and pair HNSW with IVF/PQ compression.

%% trellis:begin %%
## Source
[Open the original ↗](https://arxiv.org/pdf/1603.09320)

## Archived copy
![[hnsw-paper-clip]]
%% trellis:end %%

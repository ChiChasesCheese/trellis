---
nodes:
- ai.vector-search
- ai.rag
url: https://www.pinecone.io/learn/
tags:
- intro
- reference
- index
---
# Pinecone Learning Center

Vendor-run but genuinely the best-organized free curriculum on vector search
and RAG: the "Faiss: The Missing Manual" series explains HNSW, IVF, and PQ
with diagrams and benchmarks, and the RAG/chunking/rerankers articles cover
the retrieval pipeline end to end. Start with the vector-indexes overview.

**Extract on read:**
- ANN index families — HNSW (graph), IVF (clustering), PQ (compression) — and their recall/latency/memory trade-offs.
- Hybrid retrieval: dense vectors + keyword/sparse scores, fused rank.
- Chunking and reranking as the levers where RAG quality is actually won.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.pinecone.io/learn/)
%% trellis:end %%

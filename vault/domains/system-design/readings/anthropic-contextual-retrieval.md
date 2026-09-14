---
nodes: [ai.rag]
url: https://www.anthropic.com/news/contextual-retrieval
tags: [canonical]
---
# Introducing Contextual Retrieval (Anthropic)

The best short engineering writeup of a production RAG pipeline: why naive
chunking destroys context, measured failure rates for embeddings-only
retrieval, and the stacked fixes — contextualized chunks, BM25 hybrid
search, and reranking — each with quantified retrieval gains.

**Extract on read:**
- Chunks lose their document context; prepending generated context per chunk cuts retrieval failures sharply.
- Embeddings + BM25 beat either alone — exact identifiers still need lexical match.
- Retrieve wide then rerank to the top-k that fits the context window; and skip RAG entirely when the corpus fits.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.anthropic.com/news/contextual-retrieval)

## Archived copy
![[anthropic-contextual-retrieval-clip]]
%% trellis:end %%

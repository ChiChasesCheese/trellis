---
id: ai-hybrid-retrieval
node: ai.vector-search
type: qa
---
## Q
Pure vector retrieval in a RAG system misses queries for "error `AUTH-4012`" and part numbers. Why, and what is the standard fix?

## A
Embeddings capture **semantic similarity** but blur exact tokens — rare identifiers, SKUs, names, and negations land poorly in embedding space, while lexical search (BM25) nails them but misses paraphrases.

Fix: **hybrid retrieval** — run BM25 and vector search in parallel and merge, typically with **Reciprocal Rank Fusion** (score by rank positions, so no score-scale calibration needed), then optionally a **cross-encoder reranker** over the fused top-k for precision where it matters.

## Q zh
RAG 系统中的纯向量检索错过了"错误 `AUTH-4012`"和零件号的查询。为什么，标准的修复是什么？

## A zh
Embedding 捕获 **语义相似性** 但模糊精确 token — 罕见标识符、SKU、名称和否定在 embedding 空间中表现不佳，而词法搜索（BM25）对它们很有效但错过了释义。

修复：**混合检索** — 并行运行 BM25 和向量搜索并合并，通常使用 **倒数排名融合**（按排名位置评分，所以无需评分级别校准），然后可选地在融合的前 k 个上使用 **cross-encoder reranker** 以获得需要的地方的精度。

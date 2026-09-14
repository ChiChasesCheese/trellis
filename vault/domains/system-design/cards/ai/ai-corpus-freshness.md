---
id: ai-corpus-freshness
node: ai.vector-search
type: qa
---
## Q
How do you keep a RAG corpus fresh as source documents change, and why does upgrading the embedding model force a special migration?

## A
Freshness: drive the index from the source of truth via **CDC or an event stream** — on document update, re-chunk, re-embed, and upsert; on delete, remove vectors (deletes are easy to forget and leak stale or unauthorized content into answers).

Model upgrades: embeddings from different models live in **incompatible spaces** — you cannot query old vectors with new-model query embeddings. Upgrading means **re-embedding the entire corpus**, usually into a parallel index with a cutover, which is why embedding-model choice is sticky and re-embed cost belongs in the design.

## Q zh
随着源文档变化，如何保持 RAG 语料库新鲜，升级 embedding 模型为什么要进行特殊迁移？

## A zh
新鲜度：通过 **CDC 或事件流** 从真实数据源驱动索引 — 文档更新时，重新分块、重新 embedding、然后 upsert；删除时，删除向量（删除容易被遗忘，会导致过时或未授权的内容泄露到答案中）。

模型升级：不同模型的 embedding 存在于 **不兼容的空间** 中 — 你不能用新模型的查询 embedding 查询旧向量。升级意味着 **重新 embedding 整个语料库**，通常进入一个平行索引然后切换，这就是为什么 embedding 模型的选择具有粘性，重新 embedding 的成本应该计入设计中。

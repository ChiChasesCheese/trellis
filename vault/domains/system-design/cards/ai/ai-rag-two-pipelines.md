---
id: ai-rag-two-pipelines
node: ai.rag
type: cloze
---
RAG is two pipelines meeting at an index. **Write path** (offline/async): parse → {{c1::chunk → embed → index}}, kept fresh by subscribing to source changes via {{c2::CDC or an event stream}} — the same pattern as any derived data store. **Read path** (online): embed query → retrieve → rerank → {{c3::assemble prompt → generate}}. Most RAG quality bugs live in the {{c4::write path and retrieval}} — stale index, bad chunking, retrieval misses — not in the LLM, so debug from the index side first.

## zh
RAG 是两条管道在索引处相遇。**写入路径**（离线/异步）：解析 → {{c1::chunk → embed → index}}，通过订阅源更改通过 {{c2::CDC or an event stream}} 保持新鲜 — 与任何派生数据存储相同的模式。**读取路径**（在线）：embed 查询 → 检索 → 重新排名 → {{c3::assemble prompt → generate}}。大多数 RAG 质量错误存在于 {{c4::write path and retrieval}} — 过时索引、坏分块、检索错过 — 而不是在 LLM 中，所以先从索引侧调试。

---
id: ai-chunking-failure-modes
node: ai.rag
type: qa
---
## Q
Documents must be split into chunks before embedding. What breaks with chunks that are too big, too small, or split naively — and what does good chunking do instead?

## A
- **Too big**: one embedding averages many topics — the vector matches nothing sharply, and each hit burns context budget on mostly-irrelevant text.
- **Too small**: chunk lacks its own context ("it increased by 40%" — what did?); the answer gets **severed across chunk boundaries** so no single retrieved chunk contains it.
- **Naive fixed-size splits**: cut mid-sentence, mid-table, mid-code-block — the classic silent RAG quality killer.

Good practice: split on **document structure** (headings, paragraphs), add **overlap** between neighbors, and prepend context (title/section path, "contextual chunking") so each chunk is self-describing. Chunking is set at **index time** — changing it means re-processing the corpus.

## Q zh
文档必须先分块再 embedding。块太大、太小或分割不当会有什么问题——正确的分块方式是什么？

## A zh
- **块太大**：一个 embedding 平均了许多主题 — 向量匹配不够尖锐，每次命中都会浪费大量上下文预算在大多无关的文本上。
- **块太小**：块缺乏自身的上下文（"增加了 40%" — 增加了什么？）；答案被 **分裂在块边界上** 所以没有单个检索到的块包含完整答案。
- **朴素的固定大小分割**：在句子中间、表格中间、代码块中间切割 — 这是 RAG 质量的经典隐形杀手。

最佳实践：按 **文档结构** 分块（标题、段落），在相邻块之间添加 **重叠**，并在前面加上上下文（标题/路径、"contextual chunking"）使每个块自我描述。分块在 **索引时** 设置 — 改变它意味着重新处理语料库。

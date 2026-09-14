---
id: ai-embeddings-as-coordinates
node: ai.foundations
type: cloze
---
An **embedding** is a fixed-length vector of floats (e.g. 1,536 dimensions) an embedding model produces for a piece of text — coordinates in a space where {{c1::semantic similarity becomes geometric distance}}, so "find related content" becomes {{c2::nearest-neighbor search}} over stored vectors. Two operational facts: embeddings are computed by a **separate, cheap model call** (not the chat model), and vectors from {{c3::different embedding models are incompatible}} — you can only compare vectors produced by the same model. This is the primitive underneath all vector search.

## zh
一个 **embedding** 是 embedding 模型为文本产生的固定长度浮点向量（例如 1,536 维）— 坐标在一个空间中，其中 {{c1::semantic similarity becomes geometric distance}}，所以"查找相关内容"变成 {{c2::nearest-neighbor search}} 在存储的向量上。两个操作事实：embedding 由一个 **独立的、廉价的模型调用** 计算（不是聊天模型），{{c3::different embedding models are incompatible}} 的向量 — 你只能比较由同一个模型生成的向量。这是所有向量搜索底层的原始操作。

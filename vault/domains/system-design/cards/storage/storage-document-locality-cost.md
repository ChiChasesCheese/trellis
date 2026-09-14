---
id: storage-document-locality-cost
node: storage.nosql
type: qa
---
## Q
Document stores sell "storage locality" — the whole record in one read. What is the write-side price of that locality, and what two modeling rules does it impose?

## A
The document is stored as one contiguous blob, so most engines must **rewrite the entire document on update** — even to flip one boolean — and if the document grew, relocate it and update pointers to it. Write cost and I/O scale with **document size, not change size**.

Modeling rules that follow:

- **Keep documents small** — locality only pays when you actually use most of what you loaded; a multi-MB document makes every read *and* write haul dead weight.
- **Avoid unbounded growth** — appending forever to an embedded array (comments, event history) means ever-more-expensive rewrites; spill unbounded lists into their own records keyed by parent ID.

Reads have the mirrored problem: you always fetch the whole document even when you need one field.

## Q zh
文档存储卖点是"存储局部性（storage locality）" — 一次读取拿到整条记录。这种局部性在写侧的代价是什么，它强加了哪两条建模规则？

## A zh
文档被存成一个连续的 blob，所以大多数引擎在更新时必须**重写整个文档** — 哪怕只翻转一个布尔值 — 而且如果文档变大了，还要搬迁它并更新指向它的指针。写成本和 I/O 随**文档大小而非改动大小**增长。

由此得出的建模规则：

- **保持文档小** — 局部性只有在你真的用到所加载内容的大部分时才划算；一个几 MB 的文档让每次读*和*写都拖着死重。
- **避免无界增长** — 往嵌入数组里无限追加（评论、事件历史）意味着重写越来越贵；把无界列表拆出去，用父 ID 作键单独存储。

读侧有镜像问题：即使只需要一个字段，你也总是取回整个文档。

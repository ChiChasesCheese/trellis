---
id: problems-google-docs-single-writer-per-document
node: problems.media.google-docs
type: qa
step: 2
tags: [grown]
---
## Q
In a collaborative document editor's data model, why must exactly one server instance own the authoritative ordering for a given document at any moment, rather than letting edits for the same document be handled by whichever server instance a client happens to connect to?

## A
Concurrent edits to the same document must converge to byte-identical results on every client, and operational transformation achieves that by giving every operation a single, strictly-ordered position in a per-document history (a global monotonic revision number) that later operations are transformed against. If two different server instances could independently assign revision numbers or transform operations for the same document, there would be two competing orderings with no way to reconcile them without a second coordination layer — so the document itself, not just individual requests, is the unit of ownership and sharding.

## Q zh
在协同文档编辑器的数据模型中，为什么在任意时刻，同一篇文档的权威排序必须只归属一个服务器实例，而不能让客户端连接到哪个实例就由哪个实例处理该文档的编辑？

## A zh
同一篇文档的并发编辑必须让所有客户端最终收敛到逐字节相同的结果，而操作转换（OT）实现这一点的方式是给每个操作在该文档的历史里分配一个严格全局有序的位置（全局单调修订号），后续操作都基于这个顺序做转换。如果两个不同的服务器实例可以各自独立地为同一篇文档分配修订号或做转换，就会产生两套互相竞争、无法在不引入额外协调层的情况下调和的顺序——所以分片和归属的单位是「文档本身」，而不是单次请求。

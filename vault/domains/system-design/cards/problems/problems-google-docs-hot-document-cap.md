---
id: problems-google-docs-hot-document-cap
node: problems.media.google-docs
type: qa
step: 7
tags: [grown]
---
## Q
In a collaborative document editor, why can't a single extremely popular document (e.g. a company-wide announcement with hundreds of simultaneous editors) be relieved of its hot-spot load by sharding, the way most key-based hot spots can, and what mitigation does that force instead?

## A
Sharding by document id only balances load across different documents; it cannot split the operation stream within one document, because that document's edits must all pass through a single ordering authority to preserve the global order operational transformation depends on. The only real mitigation is a product-level limit on simultaneous active editors per document — once a document exceeds that cap, additional joiners are switched to a read-only live-updating view instead of participating in the merge, turning an architectural bottleneck into an explicit, bounded product constraint rather than pretending the system can scale one document's write throughput indefinitely.

## Q zh
在协同文档编辑器中，为什么一篇极受欢迎的文档（例如有数百人同时编辑的全公司公告）无法像大多数按 key 分片能解决的热点那样通过分片来缓解负载，这迫使采用什么样的应对手段？

## A zh
按文档 id 分片只能均衡不同文档之间的负载，无法拆分单篇文档内部的操作流，因为该文档的所有编辑都必须经过同一个排序权威节点，才能维持操作转换所依赖的全局顺序。真正可行的缓解手段是在产品层面限制单篇文档的同时活跃编辑人数上限——一旦超过这个上限，新加入者会被切换到只读的实时更新视图而不参与合并，这是把一个架构层面的瓶颈转化为一个明确、有界的产品约束，而不是假装系统能无限扩展单篇文档的写吞吐。

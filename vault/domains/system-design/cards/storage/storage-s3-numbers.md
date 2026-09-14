---
id: storage-s3-numbers
node: storage.object
type: cloze
---
S3-class object storage is designed for {{c1::11 nines (99.999999999%)}} of *durability* — achieved by erasure-coding/replicating across multiple availability zones — but its *availability* SLA is only around {{c2::99.9–99.99%}}, so callers must still handle 5xx/retries. Durability ≠ availability: your bytes survive, but you can't always read them right now.

## zh
S3 类对象存储设计为 {{c1::11 个 9（99.999999999%）}}的**持久性**——通过删除编码/复制跨多个可用性区域实现——但其**可用性** SLA 仅约 {{c2::99.9–99.99%}}，所以调用者仍须处理 5xx/重试。持久性 ≠ 可用性：你的字节存活，但你不能总是现在读到它们。

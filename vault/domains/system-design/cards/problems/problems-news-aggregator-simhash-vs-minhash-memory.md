---
id: problems-news-aggregator-simhash-vs-minhash-memory
node: problems.search.news-aggregator
type: qa
step: 2
tags: [grown]
---
## Q
In a news aggregator's near-duplicate detection design, why would a design choose a single 64-bit SimHash fingerprint per article over a multi-value MinHash signature (from shingling + LSH banding) for the primary duplicate-detection index, given both can estimate document similarity?

## A
A MinHash signature needs many hash values per document to estimate Jaccard resemblance accurately — a 128-value signature at 4 bytes each is about 512 bytes/article — while SimHash's random-hyperplane rounding compresses similarity information into a single 64-bit (8-byte) fingerprint, about 64x smaller per document. For an index that must stay resident in memory to support fast incremental cluster lookups as articles arrive continuously (rather than a one-time batch similarity computation), that memory footprint difference is decisive: at 7.2 million actively-clustered articles, the SimHash index costs about 58 MB versus roughly 3.7 GB for the equivalent MinHash signatures. MinHash retains an advantage when arbitrary similarity thresholds or asymmetric containment queries are needed, but a design that only needs a fast, safe near-duplicate check doesn't need that flexibility.

## Q zh
在一个新闻聚合器的近似重复检测设计中，两种技术都能估计文档相似度，为什么设计会选择每篇文章一个 64 位 SimHash 指纹，而不是来自 shingling + LSH banding 的多维 MinHash 签名，作为主要判重索引？

## A zh
MinHash 签名需要每篇文档保留很多个哈希值才能准确估计 Jaccard 相似度——一个 128 维、每个哈希值 4 字节的签名约 512 字节/篇——而 SimHash 的随机超平面舍入把相似度信息压缩进单个 64 位（8 字节）指纹，每篇文档体积约小 64 倍。对一个必须常驻内存以支撑文章持续到达时快速增量聚类查找（而不是一次性批量相似度计算）的索引来说，这个内存占用差距是决定性的：在 720 万篇活跃聚类文章的规模下，SimHash 索引约 58 MB，而等价的 MinHash 签名约需 3.7 GB。当需要任意相似度阈值或非对称包含关系查询时 MinHash 仍有优势，但一个只需要快速、安全判重检查的设计不需要那种灵活性。

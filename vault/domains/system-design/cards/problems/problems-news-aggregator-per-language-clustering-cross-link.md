---
id: problems-news-aggregator-per-language-clustering-cross-link
node: problems.search.news-aggregator
type: qa
step: 8
tags: [grown]
---
## Q
In a news aggregator serving multiple region/language editions, why must near-duplicate clustering stay strictly scoped per language rather than being a design choice, and how does the design still let a globally significant story benefit a smaller-language edition?

## A
The near-duplicate fingerprint is computed from language-specific tokens (shingles or words), so two articles describing the same event in different languages produce unrelated shingle sets and SimHash fingerprints purely as a consequence of how the fingerprint is built — they cannot cluster together by construction, regardless of design intent, making per-language clustering a correctness requirement rather than an optimization. To still let global stories be visible in smaller editions, a lightweight secondary linking step runs only on clusters that already cross a per-language corroboration threshold, using structured signals that don't require translation (shared wire-service tags, or named entities independently extracted in each language) to connect same-event clusters across language editions into a single global-story record; each edition's ranking score is still computed independently from its own publishers, but can borrow a modest boost from the linked global story's significance.

## Q zh
在一个服务多个地区/语言版面的新闻聚合器中，为什么近似重复聚类必须严格按语言分开而不是一个可选的设计决定？这个设计如何仍然让一个全球性重大故事惠及一个较小语言的版面？

## A zh
近似重复指纹是从语言相关的 token（shingle 或词）计算出来的，所以两篇用不同语言描述同一事件的文章，仅仅因为指纹的构造方式就会产生完全不相关的 shingle 集合和 SimHash 指纹——无论设计意图如何，它们在构造上就无法被聚到一起，这让按语言分开聚类成为一个正确性要求而不是可选的优化项。为了仍然让全球性故事在较小语言的版面里可见，一个轻量的次级关联步骤只对已经跨过单语言佐证阈值的故事运行，使用不需要翻译的结构化信号（共享的通讯社标签，或各语言独立抽取出的命名实体）把描述同一事件的不同语言故事关联成一个全球故事记录；每个版面的排序分数仍然只用该版面自己的发布方数据独立计算，但可以从关联到的全球故事的显著性里借到一点适度的加成。

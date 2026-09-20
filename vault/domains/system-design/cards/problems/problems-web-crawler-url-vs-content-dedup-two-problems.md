---
id: problems-web-crawler-url-vs-content-dedup-two-problems
node: problems.search.web-crawler
type: qa
step: 4
tags: [grown]
---
## Q
In a web crawler, why are 'have we seen this exact URL before' and 'is this content actually a duplicate of something we already crawled, reached via a different URL' two genuinely separate deduplication problems that need different techniques?

## A
URL-level deduplication (e.g. via a Bloom filter on canonicalized URLs) only catches exact or near-exact URL matches, but the same underlying content is routinely served at multiple distinct URLs — with different tracking parameters, mirrors, or session identifiers — that no URL-level check will ever recognize as related. Catching that requires content-level similarity detection, such as a similarity signature (e.g. minhash over text shingles) compared against recently-seen signatures with a distance threshold, because an exact content hash also fails whenever two pages differ in trivial ways (timestamps, ads, footers) while being substantively the same article.

## Q zh
在网络爬虫中，为什么「是否见过这个 URL」和「这份内容是否其实是已抓取过的重复内容、只是通过不同 URL 到达」是两个真正独立、需要不同技术的去重问题？

## A zh
URL 级去重（例如对规范化后的 URL 做 Bloom filter）只能捕获精确或近似相同的 URL，但同一份实质内容经常挂在多个不同的 URL 下——带不同追踪参数、镜像站点、会话标识——这些 URL 级检查永远不会识别为相关。要捕获这种情况需要内容级的相似度检测，例如基于文本 shingle 的相似度签名（如 minhash），与最近见过的签名比对相似度阈值，因为精确内容哈希在两个页面只有细枝末节不同（时间戳、广告、页脚）但实质是同一篇文章时同样会失效。

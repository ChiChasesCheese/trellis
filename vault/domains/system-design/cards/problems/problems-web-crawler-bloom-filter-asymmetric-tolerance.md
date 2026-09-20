---
id: problems-web-crawler-bloom-filter-asymmetric-tolerance
node: problems.search.web-crawler
type: qa
step: 3
tags: [grown]
---
## Q
In a web crawler's URL-seen deduplication, why is a Bloom filter an acceptable data structure despite its false-positive risk, given that the crawler's correctness requirement is 'never re-crawl a URL already seen' rather than 'never skip a URL that's actually new'?

## A
A Bloom filter can only produce false positives (occasionally claiming a genuinely new URL has already been seen, causing it to be skipped) and never false negatives (it will never claim a seen URL is new), so it structurally cannot violate the crawler's hard requirement of avoiding repeated crawls of the same URL — the only cost of its error is a small, tunable probability of missing a small fraction of new URLs. This asymmetry lets the crawler trade a tunable false-positive rate for a large memory reduction versus an exact hash set (a worked estimate found roughly 20x less memory at a 0.1% false-positive rate for a set of hundreds of billions of URLs).

## Q zh
在网络爬虫的「URL 是否见过」去重判断中，为什么尽管 Bloom filter 存在假阳性风险，它仍然是可接受的数据结构——考虑到爬虫的正确性要求是「绝不重复抓取已见过的 URL」而不是「绝不跳过真正的新 URL」？

## A zh
Bloom filter 只会产生假阳性（偶尔把一个确实是新的 URL 误判为已经见过，从而被跳过），绝不会产生假阴性（它绝不会把一个见过的 URL 判断为新的），所以它在结构上不可能违反爬虫「避免重复抓取同一 URL」这条硬性要求——它出错的唯一代价是以一个可调的小概率漏掉一小部分新 URL。这种不对称性让爬虫可以用一个可调的假阳性率换取相对精确哈希集合大得多的内存节省（一个具体估算在千亿级 URL 集合、0.1% 假阳性率下算出约 20 倍的内存节省）。

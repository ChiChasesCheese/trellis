---
id: problems-web-crawler-dns-not-the-bottleneck
node: problems.search.web-crawler
type: qa
step: 7
tags: [grown]
---
## Q
In a web crawler sized to fetch billions of pages per crawl cycle, why does DNS lookup volume typically come out roughly two orders of magnitude smaller than fetch QPS once per-host caching is in place, and what mistake does that number rule out?

## A
DNS lookups are needed per distinct host, not per URL, and a large crawl discovers vastly more URLs per host than one lookup would suggest — so once a resolved IP is cached with a TTL aligned to the crawl cycle, the number of fresh lookups needed is bounded by the number of distinct hosts, which is a small fraction of the total fetch volume. This rules out over-engineering DNS resolution as a heavyweight distributed system of its own scale to match fetch QPS; the real risk to watch for instead is stale cached entries after a host's IP changes, handled by refreshing on fetch failure rather than by building more DNS infrastructure.

## Q zh
在一个按每周期抓取数十亿页面规模设计的网络爬虫中，为什么一旦做好按宿主缓存，DNS 查询量通常会比抓取 QPS 低接近两个数量级，这个数字排除了什么样的设计错误？

## A zh
DNS 查询是按不同宿主而不是按 URL 需要的，而一次大规模抓取每个宿主发现的 URL 数量远超一次查询所暗示的量级——所以只要把解析结果按与抓取周期对齐的 TTL 缓存起来，需要的新鲜查询次数就被限制在「不同宿主数量」这个远小于总抓取量的范围内。这排除了把 DNS 解析过度设计成一套与抓取 QPS 同量级的重量级独立分布式系统的错误；真正该警惕的风险是宿主 IP 变更后缓存条目过期，应该靠抓取失败时触发刷新来处理，而不是靠建更多 DNS 基础设施。

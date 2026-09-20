---
id: problems-web-crawler-host-concurrency-sets-machine-floor
node: problems.search.web-crawler
type: qa
step: 1
tags: [grown]
---
## Q
In a distributed web crawler designed to hit a target fetch QPS while honoring a per-host politeness delay (e.g. at most one request per host every few seconds), why does the number of distinct hosts that must be fetched from concurrently, rather than the raw fetch QPS itself, usually set the actual floor on how many fetcher machines are needed?

## A
Politeness caps the sustainable request rate to any single host far below the crawler's overall target rate, so hitting a high aggregate QPS requires spreading requests across many thousands of distinct hosts in flight at once, not sending many requests to few hosts. If each fetcher machine can hold only a limited number of concurrent connections (one per in-flight host), the number of machines needed to cover enough distinct hosts simultaneously can exceed what raw QPS divided by per-machine throughput would suggest — a worked estimate can show host-concurrency requiring several times more machines than raw-QPS-based sizing alone would imply.

## Q zh
在一个分布式网络爬虫中，如果要在遵守单宿主礼貌延迟（例如同一宿主每隔几秒最多一次请求）的前提下达到目标抓取 QPS，为什么通常是「需要同时保持在途请求的不同宿主数量」、而不是原始抓取 QPS 本身，决定了实际需要多少台抓取机器？

## A zh
礼貌约束把对任意单个宿主的可持续请求速率限制在远低于爬虫整体目标速率的水平，所以要达到较高的聚合 QPS，必须把请求分散到同时在途的成千上万个不同宿主上，而不是对少数宿主发大量请求。如果每台抓取机器只能维持有限数量的并发连接（每个在途宿主占一个），那么「同时覆盖足够多不同宿主」所需要的机器数，可能会超过「原始 QPS 除以单机吞吐」算出来的数字——一个具体估算可以显示宿主并发数所要求的机器数比仅按原始 QPS 估算高出好几倍。

---
id: problems-web-crawler-politeness-caps-scale-out-not-up
node: problems.search.web-crawler
type: qa
step: 8
tags: [grown]
---
## Q
In a web crawler, why can't adding more fetcher machines increase the sustainable crawl rate against a single popular host, and what does that imply about how the system should scale to serve a much larger overall crawl target?

## A
The politeness constraint caps the request rate to any one host based on that host's own tolerance (observed via adaptive throttling), not on how much fetcher capacity the crawler has available — so no amount of additional machines lets the crawler legitimately exceed that per-host ceiling. This means scaling the system's overall throughput to a much larger target has to come from increasing the breadth of distinct hosts crawled in parallel, not from increasing the rate against any single host; at very large scale, the bottleneck shifts from machine count to how many hosts the crawler can discover and hold in flight simultaneously.

## Q zh
在网络爬虫中，为什么增加更多抓取机器不能提高对单个热门宿主的可持续抓取速率，这对系统如何扩展以服务大得多的整体抓取目标意味着什么？

## A zh
礼貌约束把对任意一个宿主的请求速率限制在该宿主自身的承受能力之内（通过自适应节流观测得到），而不是限制在爬虫拥有多少抓取能力之内——所以无论增加多少台机器，都不能让爬虫合理地超过这个单宿主速率上限。这意味着要把系统整体吞吐扩展到大得多的目标，必须靠增加并行抓取的不同宿主的广度，而不是靠提高对单一宿主的速率；在极大规模下，瓶颈会从机器数量转移到爬虫能同时发现并保持在途多少个宿主上。

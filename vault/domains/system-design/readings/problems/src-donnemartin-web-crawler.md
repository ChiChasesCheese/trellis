---
nodes: [problems.search.web-crawler]
url: https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md
tags: [engineering-blog]
---
# Web Crawler — system-design-primer

值得读：免费、MIT 协议的深度题解，给出了 `links_to_crawl`/`crawled_links` 两张表的数据模
型、用 MapReduce 对十亿级链接做频次统计去重、以及用 Jaccard/余弦相似度检测近似重复内容的
思路。本题解与它的区别在于：它把去重当成一次性批处理问题，本题解把 URL 去重设计成一个持续
运行、内存常驻的 Bloom filter，并给出了具体的位数和分片内存估算，更贴近一个持续增量抓取系
统的真实运行方式。

---
id: problems-web-crawler-spider-trap-pattern-plus-similarity
node: problems.search.web-crawler
type: qa
step: 6
tags: [grown]
---
## Q
In a web crawler, why does detecting spider traps (like infinitely-generated calendar pages) by combining URL structural pattern similarity with fetched-content similarity work better than a single global maximum crawl depth?

## A
A fixed maximum depth alone either punishes legitimate deep content that genuinely has many distinct pages (like a forum's paginated history) or misses traps that grow slowly in depth but explosively in URL count at each level (like a calendar's 'next month' links). Requiring both a high structural similarity among a host's URLs (e.g. many URLs differing only in an incrementing or date parameter) and a high content similarity among the pages actually fetched from them (via the same similarity signature used for content deduplication) targets the actual signature of a trap — many near-identical pages disguised as many distinct URLs — without penalizing genuinely deep but substantively different paginated content.

## Q zh
在网络爬虫中，为什么用「URL 结构模式相似度 + 抓取内容相似度」组合来检测蜘蛛陷阱（如无限生成的日历页面），比单一的全局最大抓取深度效果更好？

## A zh
单纯固定最大深度要么会误伤真正拥有大量不同页面的合法深层内容（比如论坛的历史分页），要么会放过深度增长缓慢但每层 URL 数量爆炸式增长的陷阱（比如日历的「下个月」链接）。同时要求「一个宿主下的 URL 结构高度相似」（例如大量 URL 只有某个递增数字或日期参数不同）和「实际抓回的内容也高度相似」（复用内容去重用的相似度签名），才能精准命中陷阱的真实特征——大量近似重复的页面伪装成大量不同的 URL——而不会误伤深度确实很深但内容确实各不相同的分页内容。

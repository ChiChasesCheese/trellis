---
id: cache-model-hit-ratio
node: caching.model
type: qa
---
## Q
A CDN reports a 95% request hit ratio but origin bandwidth remains high. What second metric explains the mismatch?

## A
Measure **byte hit ratio**. If many tiny assets hit while a few large videos miss, request hit ratio looks excellent but most bytes still come from origin. Segment both ratios by object class, POP and status, and include shield hits separately so you know whether a local miss actually reached origin.

## Q zh
CDN 报告 95% request hit ratio，但 origin bandwidth 仍很高。哪个第二指标能解释矛盾？

## A zh
测量 **byte hit ratio**。如果大量小 asset 命中、少量大 video miss，request hit ratio 很漂亮，但大部分 bytes 仍来自 origin。按 object class、POP、status 切分两种 ratio，并单独统计 shield hit，才能知道 local miss 是否真的到达 origin。

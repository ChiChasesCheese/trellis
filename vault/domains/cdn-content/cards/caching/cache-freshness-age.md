---
id: cache-freshness-age
node: caching.freshness
type: qa
---
## Q
A response has `Cache-Control: max-age=300` and arrives with `Age: 280`. How much freshness remains, and why must a downstream cache not restart the five-minute TTL?

## A
Roughly 20 seconds remain, subject to HTTP's corrected-age calculation using `Date` and transit/residence time. `Age` carries time already spent in upstream caches; restarting at 300 seconds at each tier would extend staleness with every hop and violate the origin's freshness lifetime.

## Q zh
响应带 `Cache-Control: max-age=300`，到达时 `Age: 280`。还剩多少 freshness？为什么 downstream cache 不能重新开始五分钟 TTL？

## A zh
大约还剩 20 秒，精确值还要按 HTTP 的 corrected-age calculation 纳入 `Date`、transit/residence time。`Age` 携带已在 upstream cache 消耗的时间；每个 tier 都重新计 300 秒会让 staleness 随 hop 延长，违反 origin 定义的 freshness lifetime。

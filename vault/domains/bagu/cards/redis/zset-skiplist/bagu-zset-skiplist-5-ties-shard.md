---
id: bagu-zset-skiplist-5-ties-shard
node: a.redis.zset-skiplist
type: qa
step: 5
---
## Q
**ZSet · 同分怎么排，榜单太大或单 key 成热点怎么办**｜追问

面试官：「两个主播金额相同谁排前面？如何做到『同金额先到的排前面』？榜单上亿成员或写入太集中怎么办？」

## A
**基本回答。** 同分时 ZSet 按成员名的字节序排，和谁先到无关。要「同金额先到的排前面」，把时间编进分数低位：分数 = 金额 × 2^20 + (MAX_T − 距开始秒数)，MAX_T = 2^20−1，到得越早低位越大，倒序榜里越靠前；金额不同时高位决定顺序，低位翻不了盘。score 是 double，只有 53 位整数精度，所以金额最多约 2^33，时间偏移最多约 12 天（2^20 秒）；超过不报错，2^53+1 读出来已是 2^53，排序默默出错。累加不能用 `ZINCRBY`（加数会加进时间位，低位溢出进位改坏金额），要用 Lua：读旧分、取高位金额、加新金额、用当前时间重新打包、`ZADD`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个 double 分数：能精确放下 53 位整数</text>
<rect x="8" y="28" width="200" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="108.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">金额（高 33 位）</text>
<rect x="208" y="28" width="124" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时间（低 20 位）</text>
<text x="108" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">金额越大越靠前</text>
<text x="270" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">早到 → 数大</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同样 100 元，不同到达时间：</text>
<rect x="8" y="120" width="160" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="88.0" y="138.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 20 秒到：105906155</text>
<rect x="176" y="120" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="138.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 30 秒到：105906145</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">倒序榜里大的在前，所以早到的排前面</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">低位存 MAX_T − 到达秒数，越早数越大</text>
</svg>
左边大的那段是金额，决定主要的排序；右边 20 位是时间，只在金额相同时才起作用。同样 100 元，第 20 秒到的分数 105906155，比第 30 秒到的 105906145 大。
**大榜与热点。**
- **大：** 单个 ZSet 百万级没问题，问题是大 key 的删除、迁移卡住 Redis，所以按天分 key（`rank:day:20261104`）并设过期。
- **热点：** 一个 key 在 Cluster 里只在一个分片，写入受单线程限制。先在应用里本地聚合一小段增量再写；或按主播 ID 哈希分成多个 ZSet，读时每片各取 Top-K 归并。全局 Top 100 要每片都取 100，因为前 100 可能全来自同一片。
- **名次：** 精确名次只对前几千名有意义，其余按分数段内人数估算。
**业务场景。** PK 活动里主播 A 第 20 秒累计到 100 元，分数 100×2^20+(1048575−20)=105906155；B 第 30 秒才到 100 元，分数 105906145，小 10，A 在前。若有人对 A 直接 `ZINCRBY 50`：低位 1048555+50=1048605 超过 2^20，进位使金额变 101，既不是 150，也不是想要的顺序。全站百万主播日榜按 `主播ID % 4` 分 4 个 ZSet，各取前 100 再挑全局前 100。
**容易错。**
- **以为分片后每片取少一点就行：** 会漏掉全局前列。

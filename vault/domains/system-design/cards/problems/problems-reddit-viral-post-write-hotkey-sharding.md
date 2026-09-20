---
id: problems-reddit-viral-post-write-hotkey-sharding
node: problems.social.reddit
type: qa
step: 7
tags: [grown]
---
## Q
In a forum system where a single viral post can absorb up to 50% of the site's peak vote QPS (e.g. 41,667 votes/sec out of an 83,333/sec site-wide peak), why does a single atomic counter (e.g. one Redis key incremented per vote) become risky at that concentration, and what does splitting the counter into 16 sub-counters change?

## A
A single key's throughput ceiling is bounded by what one instance can sustain (on the order of 100,000-180,000 ops/sec for a single Redis instance); 41,667 votes/sec on one key leaves a thin safety margin against jitter, GC pauses, or co-located slow commands. Splitting the target's counter into 16 independently-writable sub-counters reduces the write rate on any single sub-counter to roughly 41,667/16 ≈ 2,604/sec, and reads sum the sub-counters together — acceptable because vote counts only need to be eventually consistent, unlike inventory counters that require a single strictly-consistent value.

## Q zh
在一个论坛系统里，如果单条爆红帖子能吸走站内峰值投票 QPS 的高达 50%（比如站内峰值 83,333/秒里的 41,667 票/秒都落在它身上），为什么在这种集中度下，单个原子计数器（比如每票自增一次的单个 Redis key）会变得危险？把计数器拆成 16 个子计数器改变了什么？

## A zh
单个 key 的吞吐上限受限于单实例能承受的量级（单个 Redis 实例大约在 10 万~18 万次操作/秒这个量级）；41,667 票/秒打在一个 key 上，相对抖动、GC 暂停或同机慢命令的安全边际很薄。把该目标的计数器拆成 16 个可独立写入的子计数器，能把落在任意单个子计数器上的写入速率降到约 41,667/16 ≈ 2,604/秒，读取时把各子计数器求和即可——这是可以接受的，因为投票计数只需要最终一致，不像库存计数器那样要求严格的单一真值。

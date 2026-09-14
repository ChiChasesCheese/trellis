---
id: leetcode-q-pairs-of-songs-with-total-durations-divisible-by-60-pattern
node: arrays-hash-prefix.counting
type: qa
anki: 1787175409360
tags: [lc::1010, leetcode, pattern, recall]
---
## Q
如何在 O(n) 时间内统计数组中两数之和能被 60 整除的对数？

## A
用哈希表记录每个数对 60 取余后出现的次数。遍历数组时，对当前数 t 取余后，先查找 (60 - t) % 60 在哈希表中已出现的次数并累加到答案，再把 t 存入哈希表。关键点：用 (60 - t) % 60 而非 60 - t，避免 t=0 时目标是 60 而非 0 的边界错误。

**Evidence**

visited = defaultdict(int); res = 0; for t in time: t = t % 60; res += visited[(60 - t)%60]; visited[t] += 1

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1010%20-%20Pairs%20of%20Songs%20With%20Total%20Durations%20Divisible%20by%2060)

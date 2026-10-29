---
id: uth-redis-hyperloglog-bitmap-1-hll
node: redis.hyperloglog-bitmap
type: qa
step: 1
---
## Q
**12KB 怎么数清上亿个不同元素**｜Redis · HyperLogLog

`PFADD` / `PFCOUNT` 为什么只用固定约 12KB，就能估算任意大集合的去重数量？

## A
**背景。** 想数“今天有多少个不同的用户访问过”。精确办法是把用户都放进集合，上亿个就要几 GB。如果允许约 1% 的误差，可以换个思路，像抛硬币：连续抛出 10 次正面很罕见，看到有人做到了，说明大概已经抛了 2^10 次。把每个元素哈希成一串随机的 0 和 1，只记“见过的最长的末尾连续 0 有多长”，就能反推元素的个数。

**结构。** 16384 个寄存器，每个 6 位，共 12288 字节；元素先哈希成 64 位。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">元素 → 64 位哈希</text>
<rect x="10" y="24" width="190" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="105" y="40.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">其余位</text>
<rect x="200" y="24" width="120" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="260" y="40.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">低 14 位</text>
<text x="105" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">数末尾连续 0 的个数 + 1 = k</text>
<text x="260" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">选寄存器</text>
<text x="8" y="90" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">16384 个寄存器, 每个 6 位, 只留见过的最大 k</text>
<rect x="10" y="100" width="34" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="27" y="114.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="48" y="100" width="34" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="65" y="114.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<rect x="86" y="100" width="34" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="103" y="114.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="124" y="100" width="34" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="141" y="114.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<rect x="162" y="100" width="34" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="179" y="114.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<rect x="200" y="100" width="34" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="217" y="114.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="238" y="100" width="34" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="255" y="114.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<rect x="276" y="100" width="34" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="293" y="114.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<text x="330" y="116" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor">...</text>
<text x="8" y="146" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">末尾有 k 个 0 的哈希, 说明大约试了 2^k 个元素;</text>
<text x="8" y="162" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">16384 个寄存器取平均, 标准误差约 0.81%</text>
<text x="8" y="182" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">PFMERGE: 逐个寄存器取最大值</text>
<text x="8" y="200" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不存元素本身: 只能估数量, 不能查某个元素在不在</text>
</svg>
```

**细节。**

- 哈希低 14 位选寄存器，其余位里“末尾连续 0 的个数 + 1”只保留最大值
- 单个寄存器估得很粗，所以 16384 个取平均，标准误差约 0.81%（1.04 ÷ √16384）
- `PFMERGE` 就是逐个寄存器取最大值

**为什么。** 不存元素本身，空间与元素个数无关；代价是只能估数量，不能查元素在不在。

**对应 LeetCode：** 无直接对应的题（概率计数）

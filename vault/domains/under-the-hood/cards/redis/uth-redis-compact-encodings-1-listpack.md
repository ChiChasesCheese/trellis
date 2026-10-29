---
id: uth-redis-compact-encodings-1-listpack
node: redis.compact-encodings
type: qa
step: 1
---
## Q
**小哈希为什么不是哈希表**｜Redis · 8.10

只有几个字段的 Hash 或 ZSET，Redis 实际怎么存？

## A
**背景。** 真正的哈希表要为桶、节点、指针花内存，元素只有几个时，这些开销比数据本身还大。元素很少时，直接把它们按顺序紧挨着放在一段连续内存里，从头扫一遍反而更省、更快。

**结构。** listpack：一整段连续内存，6 字节头部（总字节数 + 元素个数），后面依次排着元素。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">listpack: 一整段连续内存</text>
<rect x="10" y="26" width="52" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="36" y="44.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">总字节</text>
<rect x="62" y="26" width="40" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="82" y="44.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">个数</text>
<rect x="108" y="26" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="110" y="28" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="125" y="44.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">编码</text>
<rect x="140" y="28" width="40" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="160" y="44.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">数据</text>
<rect x="180" y="28" width="26" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="193" y="44.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">回长</text>
<rect x="212" y="26" width="100" height="30" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<rect x="214" y="28" width="30" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="229" y="44.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">编码</text>
<rect x="244" y="28" width="40" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="264" y="44.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">数据</text>
<rect x="284" y="28" width="26" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="297" y="44.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">回长</text>
<rect x="318" y="26" width="12" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="10" y="74" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6 字节头</text>
<text x="110" y="74" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">元素 = 编码 + 数据 + 回溯长度</text>
<line x1="300" y1="90" x2="130" y2="90" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="130,90 136.0,87.3 136.0,92.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="215" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从尾往头倒着走</text>
<text x="8" y="134" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">回溯长度在元素末尾, 每个元素只记自己的长度</text>
<text x="8" y="152" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">小整数: 编码 1 字节; 短字符串: 多 1 字节长度头</text>
<text x="8" y="170" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超过阈值才转成哈希表 / 跳表:</text>
<text x="8" y="186" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Hash 512 条, ZSET 128 条, 单个值超 64 字节</text>
</svg>
```

**细节。**

- 每个元素 = 编码 + 数据 + 回溯长度（`backlen`，记着这个元素有多长），后者在元素末尾，所以能从尾往头倒着走
- 小整数只占 1 字节编码，短字符串只多 1 字节长度头
- 超过阈值才转成哈希表 / 跳表：Hash 默认 512 条，ZSET 默认 128 条，单个值超 64 字节也转

**为什么。** 元素少时，顺序扫一段连续内存比哈希表的指针、桶、节点更省内存，也更快。

**对应 LeetCode：** 无直接对应的题（紧凑内存编码）

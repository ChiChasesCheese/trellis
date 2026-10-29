---
id: uth-redis-sds-dict-1-sds
node: redis.sds-dict
type: qa
step: 1
---
## Q
**Redis 为什么不用 C 字符串**｜Redis · 8.10

Redis 的字符串底层 SDS（Simple Dynamic String）和 C 的 `char*` 比，多了什么？

## A
**背景。** C 字符串靠结尾的 `\0` 标记结束，自己不记长度：求长度要从头扫到 `\0`；内容里不能有 `\0`，存二进制数据就不行；每次追加都要先重新申请内存。Redis 的办法：在字符前面加一个小头部，记下长度和容量。

**结构。** 一段连续内存，头部存 `len`（已用）、`alloc`（容量）、`flags`（类型），指针指向头部之后的字符数据。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">SDS: 头部 + 字符数据</text>
<rect x="10" y="28" width="50" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="35" y="46.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">len</text>
<rect x="60" y="28" width="50" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="85" y="46.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">alloc</text>
<rect x="110" y="28" width="50" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="135" y="46.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">flags</text>
<rect x="160" y="28" width="24" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="172" y="46.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">h</text>
<rect x="186" y="28" width="24" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="198" y="46.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">e</text>
<rect x="212" y="28" width="24" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="224" y="46.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">l</text>
<rect x="238" y="28" width="24" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="250" y="46.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">l</text>
<rect x="264" y="28" width="24" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="276" y="46.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">o</text>
<rect x="290" y="28" width="24" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="302" y="46.5" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">\0</text>
<line x1="160" y1="58" x2="160" y2="76" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="160,76 157.3,70.0 162.7,70.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="160" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">指针指向字符数据</text>
<text x="8" y="114" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">len 已用, alloc 容量; 头部分 5 种, 长度字段 1 到 8 字节</text>
<text x="8" y="132" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">追加时预分配: 新长度 &lt; 1MB 翻倍, 否则每次多给 1MB</text>
<text x="8" y="150" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">长度 O(1) 读出; 内容里可以有 \0 (二进制安全)</text>
<text x="8" y="172" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">C 字符串求长度要扫一遍, 追加要反复 realloc</text>
</svg>
```

**细节。**

- 头部按长度分 5 种，长度字段最小 1 字节，最大 8 字节
- 追加时预分配：新长度小于 1MB 就翻倍，否则每次多给 1MB
- 长度 O(1) 读出，内容里可以有 `\0`（二进制安全）

**为什么。** C 字符串求长度要扫一遍，追加要反复 `realloc`；多几个字节的头部换来 O(1) 求长和均摊 O(1) 追加。

**对应 LeetCode：** 无直接对应的题（字符串内存布局）

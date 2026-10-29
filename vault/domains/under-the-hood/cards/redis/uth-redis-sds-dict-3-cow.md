---
id: uth-redis-sds-dict-3-cow
node: redis.sds-dict
type: qa
step: 3
---
## Q
**BGSAVE 时哈希表为什么不扩容**｜Redis · 8.10

后台保存 RDB 期间，Redis 对 `dict` 的扩容、缩容策略有什么不同？

## A
**背景。** 后台保存时，子进程和父进程共享同一批内存页，父进程改哪一页才复制那一页。而哈希表扩容会把大量元素搬来搬去，改写大量的页，会让复制出来的页暴涨，内存翻倍。

**结构。** 全局开关 `dict_can_resize` 有三档：允许、避免、禁止；父进程有子进程时设为“避免”，子进程里设为“禁止”。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">元素数 / 桶数 到多少, dict 才扩容</text>
<line x1="20" y1="100" x2="320" y2="100" stroke="currentColor" stroke-width="1"/>
<line x1="20" y1="94" x2="20" y2="106" stroke="currentColor" stroke-width="1"/>
<text x="20" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<line x1="100" y1="94" x2="100" y2="106" stroke="currentColor" stroke-width="1"/>
<text x="100" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<line x1="260" y1="94" x2="260" y2="106" stroke="currentColor" stroke-width="1"/>
<text x="260" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="8" y="56" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无子进程</text>
<line x1="100" y1="70" x2="320" y2="70" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="320,70 314.0,72.7 314.0,67.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="210" y="62" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">到 1 就扩容</text>
<text x="8" y="150" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">有子进程 (避免档)</text>
<line x1="260" y1="164" x2="320" y2="164" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="320,164 314.0,166.7 314.0,161.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="168" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只有到 4 才强制扩容</text>
<text x="8" y="188" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缩容要降到 1/32 以下才强制; 子进程里则完全禁止</text>
</svg>
```

**细节。**

- 子进程和父进程靠写时复制（copy-on-write）共享内存页
- 搬迁会改写大量页，导致子进程期间复制的页暴涨
- “避免”档下，只有元素数与桶数之比达到 4 才强制扩容，缩容要降到 1/32 以下才强制

**为什么。** 宁可让哈希链暂时变长，也不愿在快照期间让内存翻倍。

**对应 LeetCode：** 无直接对应的题（内存与快照的取舍）

---
id: uth-redis-hyperloglog-bitmap-3-bitmap
node: redis.hyperloglog-bitmap
type: qa
step: 3
---
## Q
**用一个字符串怎么做签到统计**｜Redis · Bitmap

`SETBIT` / `BITCOUNT` 底下是什么？一亿用户的签到要多少内存？

## A
**背景。** 要记一亿个用户今天有没有签到。每人用 1 个字节存“是/否”，要 100MB；每人只用 1 个二进制位，8 个用户共用一个字节，只要约 12.5MB。位图（bitmap）就是这个想法。

**结构。** 位图不是独立类型，就是普通字符串，第 0 位是第一个字节的最高位。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 195">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">位图 = 普通字符串, 一位表示一个用户</text>
<rect x="10" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="19" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="28" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="37" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="46" y="28" width="18" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="55" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="64" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="73" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="82" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="91" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="100" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="109" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="118" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="127" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="136" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="145" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<text x="82" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">字节 0</text>
<rect x="180" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="189" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="198" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="207" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="216" y="28" width="18" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="225" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="234" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="243" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="252" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="261" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="270" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="279" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="288" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="297" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="306" y="28" width="18" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="315" y="43.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<text x="252" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">字节 1</text>
<text x="8" y="92" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SETBIT key 10 1: 偏移 10 = 字节 1 的第 3 位</text>
<text x="8" y="110" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第 0 位是第一个字节的最高位</text>
<text x="8" y="130" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">一亿用户约 12.5MB; 偏移上限 2^32 - 1, 最大 512MB</text>
<text x="8" y="148" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">BITCOUNT: 有 POPCNT 指令一次数 64 位</text>
<text x="8" y="164" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否则用 0x55555555 等三个掩码分三步折叠</text>
<text x="8" y="186" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">坑: 第一次 SETBIT 很大的偏移要一次分配全部内存</text>
</svg>
```

**细节。**

- 一个用户一位：一亿用户约 12.5MB；`BITCOUNT` 统计当天签到人数
- 偏移上限 2³²−1，所以字符串最大 512MB
- `BITCOUNT`：CPU 有 `POPCNT` 指令（一条指令数出 64 位里 1 的个数）就一次数 64 位；否则用 `0x55555555`、`0x33333333`、`0x0F0F0F0F` 三步位运算折叠

**为什么。** 一位表示一个状态，空间最小，`BITOP` 还能直接求交并集。

**坑。** 第一次对很大的偏移 `SETBIT`，要一次分配前面全部内存，可能卡住服务器。

**对应 LeetCode：** 无直接对应的题（位级存储）

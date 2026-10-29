---
id: uth-python-memory-gc-4-arena
node: python.memory-gc
type: qa
step: 4
---
## Q
**del 之后内存为什么不降**｜Python · CPython 3.14.8

创建 200 万个小对象再 `del` 掉 99%，进程占用的内存会降多少？

## A
**背景。** 小对象数量极多，每次都向操作系统要内存太慢。Python 自己批发一大块，再零售给小对象；对象释放后，内存先还给 Python 自己的货架，不是立刻还给系统。

**结构。** 小对象归 pymalloc 管：64 位下向系统要 1 MiB 的竞技场（arena），切成 16 KiB 的内存页（pool）按大小分配。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="120" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">竞技场 1 MiB = 若干 16 KiB 内存页</text>
<rect x="14" y="34" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="40" y="34" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="66" y="34" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="92" y="34" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="118" y="34" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="144" y="34" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="170" y="34" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="196" y="34" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="236" y="48" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">整块空</text>
<text x="236" y="64" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">可还给系统</text>
<rect x="14" y="82" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="40" y="82" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="66" y="82" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="92" y="82" width="26" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="118" y="82" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="144" y="82" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="170" y="82" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="196" y="82" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="236" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">还剩 1 个</text>
<text x="236" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">整块不能还</text>
<rect x="14" y="130" width="26" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="40" y="130" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="66" y="130" width="26" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="92" y="130" width="26" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="118" y="130" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="144" y="130" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="170" y="130" width="26" height="30" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="196" y="130" width="26" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="236" y="144" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">仍在使用</text>
<text x="236" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="170" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚线 = 已释放的页</text>
</svg>
```

**细节。**

- 实测 200 万个短字符串占 189 MB；只留 1%，其余 `del` 后仍是 189 MB。
- 剩下的也删掉，才降到 37 MB。
- 一个竞技场里只要还有一个活对象，整块就不能还给系统。

**为什么。** 整块腾空的竞技场才能归还系统；碎片化时空闲内存只留在进程里等着复用。

**对应 LeetCode：** 无直接对应的题

---
id: uth-ai-paged-kv-3-cow
node: ai.paged-kv
type: qa
step: 3
---
## Q
**共享同一份 prompt：引用计数与写时复制**｜vLLM · PagedAttention

同一个 prompt 要生成 2 个不同的答案，prompt 的 KV 缓存要存两份吗？两个答案各写各的，怎样不互相覆盖？

## A
**背景。** 并行采样（parallel sampling）：对同一个 prompt 采出多个答案。prompt 部分的 KV 缓存完全一样，存两份纯属浪费。

**结构。** 引用计数（reference count）：每个物理块记着有几个答案在用它。两个答案的块表指向同一批物理块，计数是 2。往共享块里写时才复制（写时复制，copy-on-write）：计数大于 1，就先申请新块、拷贝内容、旧块计数减 1，再写新块；计数为 1 直接写。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="12" y="16" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同一个 prompt 抽 2 个答案</text>
<rect x="10" y="28" width="130" height="50" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="75" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">答案 A1</text>
<text x="75" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">共用块 7, 自有块 3</text>
<rect x="200" y="28" width="130" height="50" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="265" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">答案 A2</text>
<text x="265" y="68" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">共用块 7, 自有块 1</text>
<rect x="10" y="150" width="80" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="50" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">物理 3</text>
<text x="50" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">引用 1</text>
<rect x="130" y="150" width="80" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">物理 7</text>
<text x="170" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">引用 2</text>
<rect x="250" y="150" width="80" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="290" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">物理 1</text>
<text x="290" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">引用 1</text>
<line x1="45" y1="78" x2="50" y2="150" stroke="currentColor" stroke-width="1"/>
<polygon points="50,150 46.5,143.2 52.5,142.8" fill="currentColor"/>
<line x1="110" y1="78" x2="150" y2="150" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="150,150 144,145.3 149.2,142.4" style="fill:var(--accent,#3b6fd4)"/>
<line x1="230" y1="78" x2="190" y2="150" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="190,150 190.8,142.4 196,145.3" style="fill:var(--accent,#3b6fd4)"/>
<line x1="295" y1="78" x2="290" y2="150" stroke="currentColor" stroke-width="1"/>
<polygon points="290,150 287.5,142.8 293.5,143.2" fill="currentColor"/>
<text x="170" y="222" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A1 要写最后一块: 引用 2, 先复制到 3 再写</text>
</svg>
```

**细节。**

- 图里 A1 要写最后一块（块 1）：引用数是 2，于是复制出块 3，块 1 的引用数降到 1，A2 之后直接写块 1
- 只有最后那个半满的块会被复制，写满的块永远共享
- 这是 PagedAttention 的原始设计；vLLM 0.32 把 `n > 1` 的请求拆成 `n` 个独立子请求，块里仍记着 `ref_cnt`：`ref_cnt == 1` 且没有哈希才允许直接写
- 计数降到 0 的块还回空闲链表

**为什么。** 和操作系统 `fork` 之后共享内存页的写时复制是同一个思路：prompt 越长，省得越多。

**对应 LeetCode：** 无直接对应的题

---
id: uth-ai-paged-kv-1-blocks
node: ai.paged-kv
type: qa
step: 1
---
## Q
**KV 缓存怎样像内存一样分页**｜vLLM · PagedAttention

大模型每生成一个字，都要回看前面所有的字，回看用的临时数据（KV 缓存）越来越大。vLLM 怎样存它，才不浪费显存？

## A
**背景。** 模型生成第 100 个字，要用前 99 个字每一层的中间结果（键 Key 和值 Value，故称 KV 缓存）。重算太慢，就存在显存里。OPT-13B 每个 token 约 800 KB，一个请求最长 2048 个 token 就是 1.6 GB。直白做法是请求一来就按最大长度预留一整段连续显存，可没人知道会生成多长，空位别人又用不了：实测这类系统只有 20.4%–38.2% 的显存真在存 token。

**结构。** 把 KV 缓存切成固定大小的块，写到哪分到哪；每个请求有一张块表（block table），记着第几个逻辑块在哪个物理块。这就是操作系统的分页：块是页，token 是字节，请求是进程。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="12" y="16" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">连续预留: 按最长 16 格占位</text>
<rect x="20" y="24" width="18" height="24" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="38" y="24" width="18" height="24" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="56" y="24" width="18" height="24" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="74" y="24" width="18" height="24" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="92" y="24" width="18" height="24" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="110" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="128" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="146" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="164" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="182" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="200" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="218" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="236" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="254" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="272" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="290" y="24" width="18" height="24" rx="0" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="170" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只用了 5 格, 其余 11 格别人也用不了</text>
<text x="12" y="100" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">分块: 每块 4 格, 写到哪分到哪</text>
<rect x="40" y="110" width="100" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="90" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 块0 -> 物理1</text>
<rect x="170" y="110" width="100" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="220" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 块1 -> 物理6</text>
<rect x="20" y="168" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="38" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="58" y="168" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="76" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A0</text>
<text x="76" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="96" y="168" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="114" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="134" y="168" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="152" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B0</text>
<text x="152" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="172" y="168" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="190" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B1</text>
<text x="190" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="210" y="168" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="228" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="248" y="168" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="266" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A1</text>
<text x="266" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="286" y="168" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="304" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<line x1="90" y1="134" x2="76" y2="168" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="76,168 75.9,160.4 81.4,162.7" style="fill:var(--accent,#3b6fd4)"/>
<line x1="220" y1="134" x2="266" y2="168" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="266,168 258.6,166.3 262.2,161.4" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="240" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">浪费最多只在每个请求的最后一块里</text>
</svg>
```

**细节。**

- 默认 16 个 token 一块；第 `pos` 个 token 在显存里的位置 = `块表[pos // 16] * 16 + pos % 16`
- 前一块写满才分新块，每个请求最多浪费不到一块；vLLM 的 KV 显存有 96.3% 存着真实 token

**为什么。** 块一样大，任何空闲块都能给任何请求，不会「总量够，但不连续」。

**例题：** LC 2502 设计内存分配器

内存有 `n` 个单元，`allocate(size, mID)` 要找最左边连续 `size` 个空闲单元分给 `mID`，`freeMemory(mID)` 释放 `mID` 的所有单元。例：`Allocator(10)`，`allocate(1,1)` → `0`，`allocate(1,2)` → `1`。KV 缓存的块就是在做这件事，只是每块大小固定。

```python
class Allocator:
    def __init__(self, n: int) -> None:
        self.mem = [0] * n             # mem[i] 是占用该单元的 mID；mID >= 1，所以 0 表示空闲

    def allocate(self, size: int, mID: int) -> int:
        run = 0                        # 当前连续空闲单元的个数
        for i, owner in enumerate(self.mem):
            run = run + 1 if owner == 0 else 0
            if run == size:            # 第一次凑够 size 个，就是最左侧的块
                start = i - size + 1
                self.mem[start:i + 1] = [mID] * size   # 切片赋值，一次写入整块
                return start
        return -1

    def freeMemory(self, mID: int) -> int:
        freed = 0
        for i, owner in enumerate(self.mem):
            if owner == mID:           # 同一个 mID 可能分散在多个块里，全部释放
                self.mem[i] = 0
                freed += 1
        return freed
```

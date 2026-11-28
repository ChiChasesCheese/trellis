---
id: lct-learn-data-structures-8-4
node: data-structures.8.4
type: qa
step: 1
---
## Q
**常用数据结构 › 树状数组和线段树 › Lazy 线段树（有区间更新）**｜学习卡

套路是什么？

## A
**一句话。** 懒标记线段树：区间更新只在拆出的 `O(log n)` 个节点上打标记，等以后要走进子树时再下传，更新和查询都是 `O(log n)`。

下图：区间更新只停在完全被覆盖的节点上打标记，不往下走。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<line x1="170.0" y1="33" x2="95.0" y2="57" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="170.0" y1="33" x2="245.0" y2="57" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="95.0" y1="79" x2="57.5" y2="103" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="95.0" y1="79" x2="132.5" y2="103" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="245.0" y1="79" x2="207.5" y2="103" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="245.0" y1="79" x2="282.5" y2="103" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="57.5" y1="125" x2="39" y2="149" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="57.5" y1="125" x2="76" y2="149" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="282.5" y1="125" x2="264" y2="149" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="282.5" y1="125" x2="301" y2="149" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<rect x="148.0" y="11" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0,7</text>
<rect x="73.0" y="57" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95.0" y="72" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0,3</text>
<rect x="223.0" y="57" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="72" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4,7</text>
<rect x="35.5" y="103" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.5" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0,1</text>
<rect x="110.5" y="103" width="44" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="132.5" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2,3</text>
<rect x="185.5" y="103" width="44" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="207.5" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4,5</text>
<rect x="260.5" y="103" width="44" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.5" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">6,7</text>
<rect x="24" y="149" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39" y="164" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="61" y="149" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="76" y="164" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="249" y="149" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="264" y="164" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<rect x="286" y="149" width="30" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="301" y="164" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">7</text>
<text x="170" y="196" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">[1, 6] 加 v：拆成 4 个整节点，各自 s += v·长度、todo += v</text>
<text x="170" y="214" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">以后要走进它们的子树，先 push 把 todo 下传</text>
</svg>

```python
s, todo = [0] * (4 * n), [0] * (4 * n)   # 区间和 / 懒标记

def push(o, l, r):               # 下传：先结清欠孩子的账
    m = (l + r) // 2
    for c, cl, cr in (2*o, l, m), (2*o + 1, m + 1, r):
        s[c] += todo[o] * (cr - cl + 1)
        todo[c] += todo[o]
    todo[o] = 0

def go(o, l, r, L, R, v=None):   # v 给定：[L,R] 加 v；否则查和
    if L <= l and r <= R:        # 整段被覆盖：打标记或直接返回
        if v is None: return s[o]
        s[o] += v * (r - l + 1); todo[o] += v; return 0
    push(o, l, r)                # 要往下走了，先下传
    m, res = (l + r) // 2, 0
    if L <= m: res += go(2*o, l, m, L, R, v)
    if R > m: res += go(2*o + 1, m + 1, r, L, R, v)
    s[o] = s[2*o] + s[2*o + 1]   # 回溯时重算
    return res
```

**要点。**
- 为什么对？：标记表示「这一段整体欠了一次更新，孩子还没收到」；任何要读写孩子的操作先 `push`，保证看到的值都是最新的，所以标记可以一直拖着。
- LC 2502 怎么改？：`n <= 1000` 时直接数组模拟就够；想用线段树就存「最长连续空闲」，分配是区间赋值 `mID`，释放要按 `mID` 找位置，标记换成「赋值」。
- 换成区间赋值或最大值怎么改？：改三处：节点值的合并（`+` 换 `max`）、标记作用到节点（赋值直接覆盖）、标记合并（赋值取新的）；标记要有「无标记」的特殊值，不能用 `0`。

**易错点。**
- 更新或查询前没 `push`：下传前孩子是旧值，整段加 `1` 后再查其中一个子区间，读到的是加之前的值。
- 整段覆盖时只改 `s[o]` 不记 `todo[o]`：以后走进子树时孩子拿不到这次更新。
- 回溯忘了 `s[o] = s[2*o] + s[2*o+1]`：父节点停在旧值，后续整段查询出错。

**对应题目。** LC 2502 设计内存分配器

---
id: uth-storage-inverted-index-1-postings
node: storage.inverted-index
type: qa
step: 1
---
## Q
**倒排索引：词 → 有序文档号列表**｜Lucene · 10.5

搜索 `kafka AND timing` 时，Lucene 怎么找到同时含两个词的文档？文档号列表怎么存才不占地方？

## A
**背景。** 最笨的搜索是把每篇文档从头读到尾，看有没有这个词；文档一多就没法用。反过来：提前建一本“词 → 含这个词的文档号”的目录，就像书后的索引。

**结构。** 这就是倒排索引（inverted index）：每个词（term）对应一个升序的文档号列表（postings）。搜两个词同时出现，就是对两个有序列表求交集：两个指针各指一个列表，小的那边前进，相等就是命中，不用把列表全展开。图里 kafka 和 timing 的交集是 7 和 20。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 128">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个词: 升序的文档号列表</text>
<text x="8" y="58" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">kafka</text>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">timing</text>
<rect x="64" y="22" width="42" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="110" y="22" width="42" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="131" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="156" y="22" width="42" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="177" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<rect x="202" y="22" width="42" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="223" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<rect x="248" y="22" width="42" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="269" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">31</text>
<rect x="64" y="72" width="42" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85" y="88.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="110" y="72" width="42" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="131" y="88.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<rect x="156" y="72" width="42" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="177" y="88.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">35</text>
<line x1="131" y1="46" x2="85" y2="72" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="223" y1="46" x2="131" y2="72" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">AND = 双指针求交集: 7, 20</text>
</svg>
```

**细节。**

- 存的不是文档号本身，而是相邻两个的差值（7、20、31 存成 7、13、11），每 256 个一块，按块内最大差值需要的位数打包；Lucene 10.4 起块大小由 128 改成 256。
- 块里的文档足够稠密时，改存位图（每个文档一位）更省，写入器按占用空间二选一。

**为什么。** 列表有序所以差值小，位数远小于 32 位；求交集只需双指针，不用全部展开。

**例题：** LC 986 区间列表的交集

给两个闭区间列表，各自内部互不相交且已按起点排序，返回它们的交集。例：`firstList = [[0,2],[5,10],[13,23],[24,25]]`，`secondList = [[1,5],[8,12],[15,24],[25,26]]` → `[[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]`。

```python
def interval_intersection(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    i = j = 0
    ans: list[list[int]] = []
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])      # 交集左端取较大的起点
        hi = min(first[i][1], second[j][1])      # 右端取较小的终点
        if lo <= hi:                             # 闭区间：lo == hi 也是一个点
            ans.append([lo, hi])
        if first[i][1] < second[j][1]:           # 终点小的那个不可能再与对方后面的区间相交
            i += 1
        else:
            j += 1
    return ans
```

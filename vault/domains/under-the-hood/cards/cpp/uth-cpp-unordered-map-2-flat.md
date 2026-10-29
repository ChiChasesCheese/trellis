---
id: uth-cpp-unordered-map-2-flat
node: cpp.unordered-map
type: qa
step: 2
---
## Q
**为什么 flat_hash_map 比 unordered_map 快**｜C++ · Abseil Swiss table

同样是 O(1) 的哈希表，`absl::flat_hash_map` 为什么常常快好几倍？

## A
**背景。** 上一张卡的链表节点散落在堆上，每次查找都在内存里跳来跳去，CPU 缓存帮不上忙。开放寻址（open addressing）换了思路：不挂链，所有元素放进一整块数组；冲突了就去看旁边的空槽。

**结构。** Swiss table：一整块数组，先是每槽一字节的控制字节（记录这个槽是空的，还是存了哈希值的低 7 位），后面是紧挨着的槽位。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">控制字节 (每槽 1 字节)</text>
<rect x="10" y="22" width="32" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="26" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2a</text>
<rect x="46" y="22" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="62" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ff</text>
<rect x="82" y="22" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="98" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7b</text>
<rect x="118" y="22" width="32" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="134" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2a</text>
<rect x="154" y="22" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="170" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ff</text>
<rect x="190" y="22" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="206" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">05</text>
<rect x="226" y="22" width="32" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="242" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2a</text>
<rect x="262" y="22" width="32" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="278" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ff</text>
<text x="8" y="66" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">查 hash 低 7 位 = 2a: 一次比较整组, 命中 3 个候选</text>
<text x="8" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">槽位 (紧挨着的数组, 没有逐个分配)</text>
<rect x="10" y="98" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="26" y="115.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k,v</text>
<rect x="46" y="98" width="32" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="82" y="98" width="32" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="98" y="115.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k,v</text>
<rect x="118" y="98" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="134" y="115.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k,v</text>
<rect x="154" y="98" width="32" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="190" y="98" width="32" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="206" y="115.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k,v</text>
<rect x="226" y="98" width="32" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="242" y="115.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k,v</text>
<rect x="262" y="98" width="32" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="8" y="150" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只对命中的槽比较 key; 空槽 ff 不用读</text>
</svg>
```

**细节。**

- 查找时先在控制字节里一次比较一整组槽，命中才去读元素
- `unordered_map` 要走“桶数组 → 节点 → 比较 key”，至少两次随机内存访问
- 大表的最大负载因子是 7/8，空间也更省

**为什么。** 缓存友好、没有逐元素分配；代价是放弃指针稳定。

**坑。** `flat_hash_map` 在 rehash 或被移动后，元素的指针和引用全部失效。

**例题：** LC 128 最长连续序列（同类：LC 560 和为 K 的子数组）

给未排序的整数数组，求数值连续的最长序列的长度，要求 O(n)。例：`[100,4,200,1,3,2]` → `4`（`1,2,3,4`）。把所有数放进哈希集合，每一次“某个数在不在”都是 O(1) 的查询。

```python
def longest_consecutive(nums: list[int]) -> int:
    num_set = set(nums)
    best = 0
    for num in num_set:
        if num - 1 in num_set:
            continue  # 只从每段区间的起点开始向后探
        length = 1
        while num + length in num_set:
            length += 1
        best = max(best, length)
    return best
```

---
id: uth-redis-compact-encodings-3-quicklist-intset
node: redis.compact-encodings
type: qa
step: 3
---
## Q
**List 和纯整数 Set 各用什么结构**｜Redis · 8.10

`LPUSH` 的 List 为什么不是一个长 listpack？只存整数的 Set 呢？

## A
**背景。** 紧凑数组在中间插入，要把后面的字节整体搬动，越长越贵；纯链表每个元素又要多存两个指针。折中：用链表把一段一段不太长的紧凑数组串起来。只存整数的集合则更简单，排好序放进数组，用二分查找。

**结构。** List 是 quicklist：双向链表，每个节点是一个 listpack。纯整数 Set 是 intset：有序的整数数组。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">quicklist: 双向链表, 每个节点一个 listpack</text>
<rect x="10" y="26" width="84" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="52" y="44.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">listpack</text>
<line x1="94" y1="41" x2="118" y2="41" stroke="currentColor" stroke-width="1"/>
<polygon points="118,41 112.0,43.7 112.0,38.3" fill="currentColor"/>
<polygon points="94,41 100.0,38.3 100.0,43.7" fill="currentColor"/>
<rect x="118" y="26" width="84" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="160" y="44.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">listpack</text>
<line x1="202" y1="41" x2="226" y2="41" stroke="currentColor" stroke-width="1"/>
<polygon points="226,41 220.0,43.7 220.0,38.3" fill="currentColor"/>
<polygon points="202,41 208.0,38.3 208.0,43.7" fill="currentColor"/>
<rect x="226" y="26" width="84" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="268" y="44.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">listpack</text>
<text x="8" y="74" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每节点最多 8KB (list-max-listpack-size = -2)</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">intset: 有序整数数组, 按最小够用的宽度存</text>
<rect x="10" y="120" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="28" y="135.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<rect x="50" y="120" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="68" y="135.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">9</text>
<rect x="90" y="120" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="108" y="135.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">40</text>
<text x="140" y="136" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">16 位</text>
<text x="8" y="162" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">插入 70000 放不下 16 位 → 整个数组升级:</text>
<rect x="10" y="172" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="40" y="187.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5</text>
<rect x="74" y="172" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="104" y="187.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">9</text>
<rect x="138" y="172" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="168" y="187.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">40</text>
<rect x="202" y="172" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="232" y="187.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">70000</text>
<text x="8" y="210" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只升不降; 查找用二分</text>
</svg>
```

**细节。**

- quicklist 默认 `list-max-listpack-size = -2`：每个节点最多 8KB
- intset 用二分查找，元素按最小够用的宽度存：16、32 或 64 位
- 插入更大的数，整个数组升级到更宽编码，只升不降
- 整数 Set 不超过 512 个元素时用 intset

**为什么。** 一个超长 listpack 在中间插入要整体搬移；纯链表每个元素多两个指针；折中就是链表串起一段段小 listpack。

**例题：** LC 704 二分查找

给升序整数数组 `nums`（元素互不相同）和目标值 `target`，存在就返回下标，否则返回 `-1`，要求 O(log n)。例：`[-1,0,3,5,9,12]`、`target = 9` → `4`。整数集合 intset 查元素用的就是这种二分。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)                  # 搜索区间 [lo, hi)，左闭右开
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1                   # mid 太小，排除 [lo, mid]
        else:
            hi = mid                       # mid 可能就是答案，保留 [lo, mid)
    return lo if lo < len(nums) and nums[lo] == target else -1
```

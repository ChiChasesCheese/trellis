---
id: uth-storage-query-exec-3-merge-join
node: storage.query-exec
type: qa
step: 3
---
## Q
**排序归并连接：双指针**｜PostgreSQL · 18

两张表都已按连接键有序时，怎么连接最省？键有重复怎么办？

## A
**背景。** 如果两张表本来就按连接键排好了序（比如走了索引），连接就不用建哈希表。

**结构。** 归并连接（merge join）：两侧各一个游标，较小的一侧前进，相等就输出，像合并两个有序数组。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 158">
<text x="8" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">外侧</text>
<text x="8" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">内侧</text>
<rect x="60" y="24" width="44" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="82" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="108" y="24" width="44" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="156" y="24" width="44" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="178" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="204" y="24" width="44" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="60" y="100" width="44" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="82" y="116.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="108" y="100" width="44" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="116.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="156" y="100" width="44" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="178" y="116.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="204" y="100" width="44" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="226" y="116.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<line x1="130" y1="48" x2="82" y2="100" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="130" y1="48" x2="130" y2="100" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="178" y1="48" x2="82" y2="100" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="178" y1="48" x2="130" y2="100" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="82" y1="148" x2="82" y2="132" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="82,126 85.0,132.0 79.0,132.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="94" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">mark</text>
</svg>
```

**细节。**

- 代价 O(n + m)，不建哈希表；输入没排序就先排序，所以执行计划里常见 `Sort` → `Merge Join`。
- 重复键：外侧遇到每一条重复键，内侧游标都要回到该键的第一条；执行器在内侧做标记（mark），之后恢复（restore）。
- 连接条件只能是等值，形如 `outerKey = innerKey`。

**为什么。** 输入本来就有序（走了索引，或下游要 `ORDER BY`）时，比哈希连接更省，输出还自带顺序。

**例题：** LC 88 合并两个有序数组

`nums1`、`nums2` 均非递减，`nums1` 长度为 `m + n`（前 `m` 个有效，后面是占位的 `0`）。把 `nums2` 原地合并进 `nums1`，结果仍非递减。例：`nums1 = [1,2,3,0,0,0]`，`m = 3`，`nums2 = [2,5,6]`，`n = 3` → `[1,2,2,3,5,6]`。

```python
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    i, j, k = m - 1, n - 1, m + n - 1           # 三个指针都从尾部往前
    while j >= 0:                               # nums2 放完就结束，nums1 剩下的本来就在位
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
```

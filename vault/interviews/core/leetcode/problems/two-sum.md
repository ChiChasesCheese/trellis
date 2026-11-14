---
slug: two-sum
---
## Q
**LC 1 两数之和**｜Easy

在数组 `nums` 中找两个不同位置的元素，和为 `target`，返回它们的下标（保证恰有一个答案）。

## A
**一句话。** 哈希表存「值→下标」，一遍扫描时先查 `target - x` 是否出现过，再存 `x`。

**图解。** 扫到 `7` 时，`9 - 7 = 2` 已在表里，直接配对。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150">
<rect x="60" y="40" width="40" height="28" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="58.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="100" y="40" width="40" height="28" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="58.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="140" y="40" width="40" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="58.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">11</text>
<rect x="180" y="40" width="40" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="58.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<text x="52" y="58" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums</text>
<text x="80.0" y="82" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="120.0" y="82" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="160.0" y="82" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="200.0" y="82" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<polyline points="120.0,24 120.0,40" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,40.0 117.0,34.0 123.0,34.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="120.0" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<text x="232" y="58" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">target = 9</text>
<rect x="60" y="96" width="104" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="112" y="113" text-anchor="middle" font-size="11" font-family="ui-monospace,Menlo,monospace" fill="currentColor">seen = {2: 0}</text>
<text x="176" y="113" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">9 − 7 = 2 在表里</text>
<text x="176" y="136" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 返回 [0, 1]</text>
</svg>

```python
def two_sum(nums, target):
    seen = {}                    # 值 -> 下标
    for i, x in enumerate(nums):
        j = seen.get(target - x)
        if j is not None:        # 先查，只会配到前面的元素
            return [j, i]
        seen[x] = i              # 后存，不会自己配自己
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先存后查：`[3,2,4]`、`target=6` 返回 `[0,0]`（`3` 用了两次）。
- 写成 `if j:`：下标 `0` 被当成没找到，`[2,7]`、`9` 返回空。

**追问。**
- 数组已有序（LC 167）？：左右双指针，`O(n)` 时间 `O(1)` 空间。
- 要返回所有不重复的数值对？：用 `Counter`，`x` 与 `target-x` 相同时要求至少出现两次。

**同模式。** LC 167 两数之和 II、LC 15 三数之和、LC 653 两数之和 IV、LC 560 和为 K 的子数组

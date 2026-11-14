---
slug: widest-possible-fence
---
## Q
**LC 4007 栅栏的最宽宽度**｜Medium

木板高度 `planks`（至多 1000 块），每块可单用，或把两块不同的木板拼成高度之和的一块，每块至多用一次。求能凑出的同高木板最多块数。

## A
**一句话。** 枚举目标高度 `h`：高 `h` 的木板单用，其余只能两两配成和为 `h`，不同高度对互不冲突；对所有高度对把配对数累加到它们的和上。

```python
def maximum_width(planks):
    cnt = Counter(planks)
    vals = sorted(cnt)
    width = Counter(cnt)            # 单用的木板
    for i, a in enumerate(vals):
        for b in vals[i:]:          # 两块拼成 a + b
            if a == b:
                width[a + b] += cnt[a] // 2
            else:
                width[a + b] += min(cnt[a], cnt[b])
    return max(width.values())
```

**复杂度。** 时间 `O(d^2)`，空间 `O(d^2)`，`d` 为不同高度数。

**易错点。**
- 同高两块配对用 `min(cnt, cnt)`：同一种高度两两配，只有 `cnt // 2` 对。
- 以为单用和拼接会抢木板：高 `h` 的木板拼接后会超过 `h`，不会参与和为 `h` 的配对。

**追问。**
- 为什么不同高度对互不冲突？：和为 `h` 时，`a` 只能配 `h - a`，每种高度只属于一对。
- 候选高度为什么只看这些？：答案高度要么是某块木板的高度，要么是两块之和，其余高度宽度为 `0`。

**同模式。** LC 1 两数之和、LC 1679 K 和数对的最大数目、LC 1711 大餐计数

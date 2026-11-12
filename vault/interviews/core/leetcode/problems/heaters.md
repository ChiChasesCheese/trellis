---
slug: heaters
---
## Q
**LC 475 供暖器**｜Medium

房屋和供暖器在一条直线上，供暖器半径相同。求能覆盖所有房屋的最小半径。

## A
**一句话。** 供暖器排序后，二分找每个房屋左右两个最近的供暖器，答案是各房屋最近距离的最大值。

```python
def find_radius(houses, heaters):
    heaters.sort()
    r = 0
    for h in houses:
        i = bisect_left(heaters, h)    # 第一个 >= h 的供暖器
        left = h - heaters[i-1] if i > 0 else inf
        right = heaters[i] - h if i < len(heaters) else inf
        r = max(r, min(left, right))
    return r
```

**复杂度。** 时间 `O((n + m) log m)`，空间 `O(1)`。

**易错点。**
- 只看一侧的供暖器：`houses=[1,5]`、`heaters=[2]` 时 `5` 只有左侧候选，缺的一侧用 `inf`。
- 最近距离取最小：`[1,5]`、`[2]` 会得 `1`，应取最大得 `3`。

**追问。**
- 供暖器半径各不相同呢？：每个供暖器是一个区间，改为区间覆盖问题。
- 也可以用双指针吗？：房屋也排序后，供暖器指针只前进不后退，免去二分。

**同模式。** LC 658 找到 K 个最接近的元素、LC 744 寻找比目标字母大的最小字母、LC 1011 在 D 天内送达包裹的能力

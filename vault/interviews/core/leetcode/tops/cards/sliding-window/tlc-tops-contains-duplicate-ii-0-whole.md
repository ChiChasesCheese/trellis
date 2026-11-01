---
id: tlc-tops-contains-duplicate-ii-0-whole
node: sliding-window.contains-duplicate-ii
type: qa
---
## Q
**LC 219 存在重复元素 II**｜Easy · 全公司热度第 165 名 · Top Interview 150

给你整数数组 `nums` 和整数 `k`，判断数组中是否存在两个**不同**的下标 `i`、`j`，满足 `nums[i] == nums[j]` 且 `abs(i - j) <= k`，存在返回 `true`，否则返回 `false`。`1 <= nums.length <= 10^5`，`-10^9 <= nums[i] <= 10^9`，`0 <= k <= 10^5`。例：`nums = [1,2,3,1]`, `k = 3` → `true`；`nums = [1,0,1,1]`, `k = 1` → `true`；`nums = [1,2,3,1,2,3]`, `k = 2` → `false`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 哈希表记录每个值最近一次出现的下标（或定长滑动窗口 + 集合）。

**一句话。** 从左到右扫，字典记每个值上一次出现的位置；遇到相同值时看与上次的距离是否 `<= k`，无论命中与否都把位置更新为当前下标。

**识别。** 「两个相等元素之间的下标距离有上限」= 对每个值只关心**最近**的那次出现；`n = 10^5` 要求 `O(n)`。

**推导。** 暴力：每个元素往后看 `k` 个，`O(nk)`，最坏 `10^10`。对当前元素 `x`，所有更早的相同值里，最近的一个离它最近，只要最近的都 `> k`，更早的更不可能；所以每个值只留一个下标，更新成当前下标就可以。

```python
def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    last: dict[int, int] = {}  # 值 -> 它最近一次出现的下标
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:  # 与最近一次相同值的距离 <= k 即命中
            return True
        last[x] = i  # 不管有没有命中都要更新：后面的重复离最近的这个才最近
    return False
```

运行：三个示例依次得到 `True`、`True`、`False`；`([1], 0)` → `False`；`([1,1], 0)` → `False`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**拓展优化。**
- 内存受限时用定长窗口：集合里只放最近 `k` 个元素，空间 `O(min(n, k))`：

```python
def contains_nearby_duplicate_window(nums: list[int], k: int) -> bool:
    window: set[int] = set()  # 恰好是下标 i-k .. i-1 的元素
    for i, x in enumerate(nums):
        if i > k:
            window.discard(nums[i - k - 1])  # 下标差已经 > k，移出窗口
        if x in window:
            return True
        window.add(x)
    return False
```

**易错点。**
- 只在第一次遇到时记录下标（`setdefault`）：`[1,0,1,1]`, `k = 1` 里 `1` 的下标一直是 `0`，`2 - 0 = 2 > 1`、`3 - 0 = 3 > 1`，返回 `False`，正确是 `True`（下标 `2` 和 `3`）。
- 边界写成 `< k`：`[1,2,3,1]`, `k = 3` 里距离恰好是 `3`，会返回 `False`，正确是 `True`。
- `k = 0` 时要求两个不同下标且距离为 `0`，不可能，答案恒为 `False`；上面两种写法都自然满足。

**同模式。** LC 217 存在重复元素、LC 220 存在重复元素 III、LC 3 无重复字符的最长子串、LC 1 两数之和。

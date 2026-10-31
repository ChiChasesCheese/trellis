---
id: tlc-patterns-hashing-5-variants
node: patterns.hashing
type: qa
step: 5
---
## Q
**哈希（Hashing）｜五种变形**

哈希题有哪几种常见形态？每种里「键」和「值」分别是什么，模板怎么改？

## A
1. **补数查找**：键 = 元素值，值 = 下标；查 `target - x`。变形：三数之和（排序 + 双指针更合适）、和为 `k` 的子数组（键 = 前缀和，值 = 出现次数）（例：LC 1 两数之和）。
2. **频次统计**：`Counter`；比较两个窗口的计数、取前 `k` 大（例：LC 347 前 K 个高频元素）。
3. **签名分组**：键 = 归一化形状。字母异位词用 26 个字母的计数 `tuple` 当键（排序后的字符串也行）；统计不同形状的岛屿时，DFS 记录每个格子相对起点的偏移，排序后转 `tuple` 放进 `set`（例：LC 49 字母异位词分组）。
4. **集合判存在 / 去重**：只关心「有没有」，用 `set`；定位序列起点用 `x - 1 not in s`（例：LC 128 最长连续序列）。
5. **点 / 对作为键**：把坐标 `(x, y)` 放进 `set`，枚举对角线上的两点，检查另两个角是否存在，时间 `O(n^2)`，`n <= 500` 可行（例：LC 939 最小面积矩形）。

**例题：** LC 1 两数之和

整数数组 `nums` 和 `target`，返回和为 `target` 的两个数的下标，恰有一个答案，`2 <= nums.length <= 10^4`。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:
            return [j, i]
        seen[x] = i
    return []
```

**例题：** LC 347 前 K 个高频元素

返回数组中出现频率前 `k` 高的元素，答案唯一，`1 <= nums.length <= 10^5`，时间要优于 `O(n log n)`。

```python
from collections import Counter
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for x, c in count.items():
        buckets[c].append(x)
    ans: list[int] = []
    for bucket in reversed(buckets):
        ans.extend(bucket)
        if len(ans) >= k:
            return ans[:k]
    return ans
```

**例题：** LC 49 字母异位词分组

把字符串数组里互为字母异位词的字符串分到一组，`1 <= strs.length <= 10^4`，字符串仅小写字母。

```python
from collections import defaultdict
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())
```

**例题：** LC 128 最长连续序列

在未排序的整数数组里找数字连续的最长序列的长度，要求 `O(n)`，`0 <= nums.length <= 10^5`。

```python
def longest_consecutive(nums: list[int]) -> int:
    seen = set(nums)
    best = 0
    for x in seen:
        if x - 1 in seen:
            continue
        end = x + 1
        while end in seen:
            end += 1
        best = max(best, end - x)
    return best
```

**例题：** LC 939 最小面积矩形

平面上的点（互不相同，`1 <= points.length <= 500`），求边平行于坐标轴的矩形的最小面积，不存在返回 `0`。

```python
from itertools import combinations
def min_area_rect(points: list[list[int]]) -> int:
    pts = [tuple(p) for p in points]
    seen = set(pts)
    areas = (
        abs(x1 - x2) * abs(y1 - y2)
        for (x1, y1), (x2, y2) in combinations(pts, 2)
        if x1 != x2 and y1 != y2 and (x1, y2) in seen and (x2, y1) in seen
    )
    return min(areas, default=0)
```

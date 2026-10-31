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
5. **点 / 对作为键**：把「方向」`(dx, dy)` 约去公约数、统一符号后放进 `Counter`，固定一个点、枚举其余所有点，同方向的点共线，时间 `O(n^2)`，`n <= 300` 可行（例：LC 149 直线上最多的点数）。

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

**例题：** LC 149 直线上最多的点数

给一个数组 `points`，`points[i] = [xi, yi]` 是平面上的一个点（`1 <= points.length <= 300`，`-10^4 <= xi, yi <= 10^4`，所有点互不相同），返回同在一条直线上的点的最大个数。

```python
from collections import Counter
from math import gcd

def max_points(points: list[list[int]]) -> int:
    best = min(len(points), 2)                 # 任意两点必共线
    for i, (x1, y1) in enumerate(points):
        direction: Counter[tuple[int, int]] = Counter()
        for x2, y2 in points[i + 1:]:          # 只看编号更大的点：每条直线从它编号最小的点数起
            dx, dy = x2 - x1, y2 - y1
            g = gcd(dx, dy)                    # 约分后同一方向只有一种写法，不用浮点斜率
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy              # 统一方向：(1, 2) 和 (-1, -2) 是同一条线
            direction[(dx, dy)] += 1
        if direction:
            best = max(best, max(direction.values()) + 1)   # 加上基准点本身
    return best
```

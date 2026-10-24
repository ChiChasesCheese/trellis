---
id: tlc-patterns-sliding-window-2-template
node: patterns.sliding-window
type: qa
step: 2
---
## Q
**滑动窗口（Sliding Window）｜模板**

写出求「最长」和「最短」两种可变窗口的模板，说明答案应该在循环的哪个位置更新。

## A
统一骨架：**右端逐个前进，把新元素纳入窗口；再用 `while` 调整左端；在合适的位置更新答案。**

**最长**（LC 340 至多 `k` 种不同字符）：违反约束才缩，缩完更新答案。

```python
from collections import Counter
def longest_k_distinct(s: str, k: int) -> int:
    cnt: Counter[str] = Counter()
    left = best = 0
    for right, ch in enumerate(s):
        cnt[ch] += 1
        while len(cnt) > k:                # 违反约束：缩左端直到恢复
            c = s[left]
            cnt[c] -= 1
            if cnt[c] == 0:
                del cnt[c]                 # 删掉计数为 0 的键，len(cnt) 才是种类数
            left += 1
        best = max(best, right - left + 1) # 约束恢复后，窗口一定合法
    return best
```

运行：`("eceba", 2)` → `3`；`("aa", 1)` → `2`；`("abc", 0)` → `0`。

**最短**（LC 209，元素为正数）：满足约束才缩，缩的过程中更新答案。

```python
def min_sub_len(target: int, nums: list[int]) -> int:
    left = total = 0
    best = len(nums) + 1
    for right, x in enumerate(nums):
        total += x
        while total >= target:             # 窗口合法：尽量缩小
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
```

运行：`(7, [2,3,1,2,4,3])` → `2`；`(4, [1,4,4])` → `1`；`(11, [1]*8)` → `0`。

规律：最长在 `while` **之后**更新（此时窗口合法），最短在 `while` **之内**更新（刚好合法的时刻）。每个下标至多进、出窗口一次，时间 `O(n)`。

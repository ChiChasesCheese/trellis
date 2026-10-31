---
id: tlc-fruit-into-baskets-2-code
node: p2.fruit-into-baskets
type: qa
step: 2
---
## Q
**LC 904 水果成篮**｜写出 Python 实现

整数数组 `fruits`（长度 `1..10^5`，`0 <= fruits[i] < fruits.length`）。求最长的连续子数组，使其中最多出现**两种**不同的数，返回它的长度。要求 `O(n)`。

## A
**思路。** `right` 逐个吞进水果并在 `Counter` 里加一；只要窗口里的种类数 `len(count)` 超过 2，就从左端吐出水果、计数减一，减到 0 时删键，直到只剩两种。每轮收缩之后窗口合法，用它的长度更新答案。

```python
def total_fruit(fruits: list[int]) -> int:
    count: Counter[int] = Counter()        # 窗口内 种类 -> 数量
    best = left = 0
    for right, kind in enumerate(fruits):
        count[kind] += 1
        while len(count) > 2:              # 超过两个篮子：收缩左端直到只剩两种
            gone = fruits[left]
            count[gone] -= 1
            if count[gone] == 0:
                del count[gone]            # 必须删键，len(count) 才是「种类数」
            left += 1
        best = max(best, right - left + 1)
    return best
```

运行：`fruits=[1,2,1]` → `3`，`fruits=[0,1,2,2]` → `3`，`fruits=[1,2,3,2,2]` → `4`，`fruits=[3,3,3,1,2,1,1,2,3,3,4]` → `5`，`fruits=[7]` → `1`。

**复杂度。** 时间 `O(n)`：`right` 走 `n` 步，`left` 总共前进不超过 `n` 步；空间 `O(1)`：`count` 最多同时有 3 个键（刚加入第三种、尚未收缩时）。

**写法要点。** `Counter()` 读写缺失键都方便；`len(count)` 直接给出种类数的前提是减到 0 就 `del`；`while` 而不是 `if` 收缩——一次右移可能需要连续吐出多个水果（`[1,1,1,2,3]`，加入 `3` 要吐三个 `1`）；`enumerate` 同时拿到下标和种类；`best = left = 0` 对不可变整数做链式初始化是安全的。

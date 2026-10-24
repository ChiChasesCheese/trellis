---
id: tlc-python-bisect-sorted-3-key-answer
node: python.bisect-sorted
type: qa
step: 3
---
## Q
**Python 工具箱｜`key` 参数与「对答案二分」**

`bisect` 的 `key` 参数（3.10+）解决什么问题？怎样用 `bisect_left(range(...), True, key=...)` 一行完成「最小的满足条件的数」？

## A
`key` 对**列表里的元素**求值再比较，被查找的 `x` 本身不经过 `key`。

```python
from bisect import bisect_left, bisect_right
pairs = [(1, "a"), (3, "b"), (3, "c"), (7, "d")]
print(bisect_left(pairs, 3, key=lambda p: p[0]))   # 1：按第一项查，x 直接写 3
print(bisect_left(pairs, (3,)))                    # 1：旧写法，(3,) 比任何 (3, ...) 都小
print(bisect_right(pairs, (3, "z")))               # 3
```

**对答案二分**：`range` 对象支持下标和 `len`，不占内存；让 `key` 返回布尔值，`False < True`，布尔序列「前面全 False、后面全 True」就是有序的，`bisect_left(..., True, ...)` 找到第一个 `True`。

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    ok = lambda k: sum(-(-p // k) for p in piles) <= h    # 速度 k 能否在 h 小时内吃完
    return bisect_left(range(1, max(piles) + 1), True, key=ok) + 1
print(min_eating_speed([3, 6, 7, 11], 8))        # 4
print(min_eating_speed([30, 11, 23, 4, 20], 5))  # 30
print(min_eating_speed([30, 11, 23, 4, 20], 6))  # 23
```

- 前提是判定函数**单调**（速度越大越可行）；加 `+1` 是因为 `range` 从 1 起，返回的是下标。
- `-(-p // k)` 是向上取整除法，不用 `math.ceil` 避免浮点。
- 适用：LC 875 爱吃香蕉的珂珂、LC 1011 运送包裹、LC 69 平方根。

**坑**：判定函数不单调时结果无意义；`key` 在 3.10 之前不可用，旧环境要手写二分。

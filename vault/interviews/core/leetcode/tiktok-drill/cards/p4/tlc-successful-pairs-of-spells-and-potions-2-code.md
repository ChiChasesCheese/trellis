---
id: tlc-successful-pairs-of-spells-and-potions-2-code
node: p4.successful-pairs-of-spells-and-potions
type: qa
step: 2
---
## Q
**LC 2300 咒语和药水的成功对数**｜写出 Python 实现

正整数数组 `spells`（长度 `n`）、`potions`（长度 `m`），均满足 `1 <= n, m <= 10^5`，元素 `1` 到 `10^5`；整数 `success`（`1 <= success <= 10^10`）。对每个咒语，返回与它的乘积 `>= success` 的药水数量。

## A
**思路。** 药水排序。对咒语 `s`，用 `bisect_left` 在有序药水里找第一个满足 `p * s >= success` 的位置，`key` 参数让二分直接比较乘积；个数是 `m` 减去这个位置。

```python
from bisect import bisect_left


def successful_pairs(spells: list[int], potions: list[int], success: int) -> list[int]:
    potions = sorted(potions)
    m = len(potions)
    # 对每个咒语 s：在有序药水里找第一个满足 p * s >= success 的位置，其右边全部成功
    return [m - bisect_left(potions, success, key=lambda p: p * s) for s in spells]
```

运行：`([5,1,3], [1,2,3,4,5], 7)` → `[4, 0, 3]`；`([3,1,2], [8,5,8], 16)` → `[2, 0, 2]`；`([1], [1], 1)` → `[1]`；`([1], [1], 2)` → `[0]`。

**复杂度。** 时间 `O((n + m) log m)`：排序一次，每个咒语一次二分；空间 `O(m)`。

**写法要点。** `bisect_left(a, x, key=f)` 把 `f` 应用到 `a` 的元素上再与 `x` 比较（Python 3.10+），`x` 本身不会被套 `f`，所以这里 `x` 直接写 `success`；列表推导里的 `lambda` 捕获的是当前循环的 `s`，因为 `bisect_left` 在同一次迭代内立刻用完，不会出现延迟绑定问题；`sorted(potions)` 生成新列表，不改变调用者的数据。

---
id: tlc-patterns-prefix-sum-2-template
node: patterns.prefix-sum
type: qa
step: 2
---
## Q
**前缀和与差分（Prefix Sum）｜模板**

写出「前缀和 + 哈希」统计和为 `k` 的子数组个数的模板，以及静态区间和与差分数组的写法。

## A
**前缀和 + 哈希（LC 560）**：`cnt[v]` = 到目前为止前缀和等于 `v` 的次数。

```python
from collections import Counter
def subarray_sum(nums: list[int], k: int) -> int:
    cnt = Counter({0: 1})              # 空前缀的和为 0，出现 1 次
    pre = ans = 0
    for x in nums:
        pre += x
        ans += cnt[pre - k]            # 以当前元素结尾、和为 k 的子数组个数
        cnt[pre] += 1                  # 先累计答案，再登记当前前缀
    return ans
```

运行：`[1,1,1], k=2` → `2`；`[1,2,3], k=3` → `2`；`[], k=0` → `0`。时间、空间都是 `O(n)`。

**静态区间和**：`pre = [0, *accumulate(nums)]`，区间 `[l, r)` 的和 = `pre[r] - pre[l]`。

**差分**：区间 `[l, r]` 加 `v`：

```python
from itertools import accumulate
def range_add(n: int, updates: list[tuple[int, int, int]]) -> list[int]:
    diff = [0] * (n + 1)
    for l, r, v in updates:
        diff[l] += v
        diff[r + 1] -= v               # 在 r+1 处把增量撤掉
    return list(accumulate(diff[:n]))  # 前缀和还原
print(range_add(5, [(1, 3, 2), (2, 4, 3), (0, 0, 1)]))   # [1, 2, 5, 5, 3]
```

前缀和与差分互为逆运算：对差分数组求前缀和得到原数组，对原数组做相邻差得到差分数组。

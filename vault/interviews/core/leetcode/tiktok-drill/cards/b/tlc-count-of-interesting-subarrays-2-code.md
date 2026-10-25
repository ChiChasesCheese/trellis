---
id: tlc-count-of-interesting-subarrays-2-code
node: b.count-of-interesting-subarrays
type: qa
step: 2
---
## Q
**LC 2845 统计趣味子数组的数目**｜写出 Python 实现

整数数组 `nums`（`1 <= 长度 <= 10^5`，`1 <= nums[i] <= 10^9`）、`modulo`（`1 <= modulo <= 10^9`）、`k`（`0 <= k < modulo`）。统计子数组的个数，使得其中满足 `nums[i] % modulo == k` 的元素个数 `cnt` 也满足 `cnt % modulo == k`。

## A
**思路。** `pre` 表示到当前位置为止「被标记元素个数」对 `modulo` 取模的结果。用 `Counter` 记录之前所有前缀余数出现的次数，初始放入空前缀 `{0: 1}`。每读一个元素，更新 `pre`，累加 `seen[(pre - k) % modulo]`，再把当前 `pre` 记入。

```python
from collections import Counter


def count_interesting_subarrays(nums: list[int], modulo: int, k: int) -> int:
    seen: Counter[int] = Counter({0: 1})           # 前缀计数（对 modulo 取模）出现的次数，空前缀算一次
    pre = ans = 0
    for x in nums:
        pre = (pre + (x % modulo == k)) % modulo   # 到当前位置，满足条件的元素个数 mod modulo
        ans += seen[(pre - k) % modulo]            # 需要某个旧前缀 p 使得 (pre - p) % modulo == k
        seen[pre] += 1
    return ans
```

运行：`([3,2,4], 2, 1)` → `3`；`([3,1,9,6], 3, 0)` → `2`；`([5], 1, 0)` → `1`；`([1,1,1], 2, 1)` → `4`；`10^5` 个元素、`modulo = 1` 时得到 `5000050000`。

**复杂度。** 时间 `O(n)`：每个元素常数次哈希操作；空间 `O(min(n, modulo))`。

**写法要点。** `(x % modulo == k)` 是 `bool`，可以直接加到整数上，省去 `if`；`Counter({0: 1})` 一步放入空前缀；`seen[...]` 读取不存在的键返回 `0`，且不会插入该键（`Counter` 与 `defaultdict` 不同）；Python 的 `%` 对负数返回非负余数，所以 `(pre - k) % modulo` 不会出现负的键，不需要像 C++ 那样再加 `modulo`。

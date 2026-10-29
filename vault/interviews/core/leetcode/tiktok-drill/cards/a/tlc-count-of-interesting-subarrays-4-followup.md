---
id: tlc-count-of-interesting-subarrays-4-followup
node: a.count-of-interesting-subarrays
type: qa
step: 4
---
## Q
**LC 2845 统计趣味子数组的数目**｜追问

面试官接着问：（1）`modulo` 很小，能不能不用哈希表？（2）要求子数组长度至少为 `2`？（3）条件换成「元素之和对 `modulo` 同余」，代码怎么改？

## A
1. **`modulo` 小**：把 `Counter` 换成长度为 `modulo` 的列表 `seen = [0] * modulo`，`seen[0] = 1`。数组访问比哈希快，且没有哈希冲突的常数。`modulo` 大到 `10^9` 时仍用字典。
2. **最短长度限制**：「延迟登记」前缀。要求长度至少为 `L`，就让位置 `r` 查询时只能用到 `l <= r - L` 的前缀：把前缀余数记入 `seen` 的时机推迟 `L` 步，下面是 `L = 2` 的写法：

```python
from collections import Counter


def count_min_len(nums: list[int], modulo: int, k: int, min_len: int = 2) -> int:
    n = len(nums)
    pres = [0] * (n + 1)                                  # pres[i]：前 i 个元素的标记数 mod modulo
    for i, x in enumerate(nums):
        pres[i + 1] = (pres[i] + (x % modulo == k)) % modulo
    seen: Counter[int] = Counter()
    ans = 0
    for r in range(min_len, n + 1):
        seen[pres[r - min_len]] += 1                      # 只登记与 r 至少隔 min_len 的前缀
        ans += seen[(pres[r] - k) % modulo]
    return ans
```

   `([3,2,4], 2, 1)` 在 `min_len = 2` 时得到 `2`（`[3,2]` 与 `[3,2,4]`）。
3. **元素之和同余**：把 `(x % modulo == k)` 换成元素值 `x`，`pre = (pre + x) % modulo`，查询键仍是 `(pre - k) % modulo`；`k = 0` 就是 LC 974（和可被 `modulo` 整除）。

**Python 提醒**：Python 的 `%` 总是返回与除数同号的结果（对正的 `modulo` 返回非负数），所以 `(pre - k) % modulo` 直接可用；C++ / Java 的 `%` 对负被除数返回负数，要写成 `((pre - k) % modulo + modulo) % modulo`。

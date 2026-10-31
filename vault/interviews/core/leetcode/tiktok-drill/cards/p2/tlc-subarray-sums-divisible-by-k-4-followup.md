---
id: tlc-subarray-sums-divisible-by-k-4-followup
node: p2.subarray-sums-divisible-by-k
type: qa
step: 4
---
## Q
**LC 974 和可被 K 整除的子数组**｜追问

面试官接着问：（1）改成和**恰好等于** `k`（LC 560）？（2）只要判断是否存在长度至少为 `2`、和是 `k` 的倍数的子数组（LC 523）？（3）求这类子数组的**最大长度**？

## A
1. **和等于 `k`。** 不取模，键就是前缀和本身，当前前缀 `p` 需要找之前出现过多少个 `p - k`：
```python
from collections import Counter

def subarray_sum(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})
    prefix = ans = 0
    for x in nums:
        prefix += x
        ans += seen[prefix - k]
        seen[prefix] += 1
    return ans
```
`([1,1,1], 2)` → `2`，`([1,2,3], 3)` → `2`。
2. **长度至少 2 的倍数和。** 字典记每个余数**第一次**出现的下标（初始 `{0: -1}`）；再遇到相同余数时，若下标差 `>= 2` 就存在：
```python
def check_subarray_sum(nums: list[int], k: int) -> bool:
    first = {0: -1}
    s = 0
    for i, x in enumerate(nums):
        s = (s + x) % k
        if s in first:
            if i - first[s] >= 2:
                return True
        else:
            first[s] = i                    # 只记第一次：保证下标差尽量大
    return False
```
`([23,2,4,6,7], 6)` → `True`，`([23,2,6,4,7], 13)` → `False`。
3. **最长长度。** 同样记第一次出现的下标，遇到相同余数取下标差的最大值；`[4,5,0,-2,-3,1]`、`k = 5` 得到 `6`（整个数组）。

**Python 提醒**：`Counter` 读取不存在的键返回 `0` 但不插入；`defaultdict(int)` 读取不存在的键会**插入**该键，字典因此变大，在“只想看看有没有”的场景里别混用。

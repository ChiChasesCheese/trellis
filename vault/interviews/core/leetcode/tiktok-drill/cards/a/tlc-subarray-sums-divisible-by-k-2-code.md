---
id: tlc-subarray-sums-divisible-by-k-2-code
node: a.subarray-sums-divisible-by-k
type: qa
step: 2
---
## Q
**LC 974 和可被 K 整除的子数组**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `3 * 10^4`，元素 `-10^4` 到 `10^4`）和整数 `k`（`2` 到 `10^4`），返回元素之和可被 `k` 整除的非空连续子数组的个数。要求 `O(n)`。

## A
**思路。** 逐个累加前缀和并立刻对 `k` 取模，用计数字典记录每个余数出现的次数（含空前缀的余数 `0`）。每个新前缀的余数在字典里已出现 `c` 次，就贡献 `c` 个以它结尾的合法子数组。

```python
from collections import Counter

def subarrays_div_by_k(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})                  # 前缀和模 k 的出现次数；空前缀的余数是 0
    prefix = ans = 0
    for x in nums:
        prefix = (prefix + x) % k           # Python 的 % 对负数也返回 [0, k)，不用再补 + k
        ans += seen[prefix]                 # 以当前位置结尾、余数相同的前缀每个对应一个合法子数组
        seen[prefix] += 1
    return ans
```

运行：`([4,5,0,-2,-3,1], 5)` → `7`，`([5], 9)` → `0`，`([-1,2,9], 2)` → `2`，`([0], 2)` → `1`。

**复杂度。** 时间 `O(n)`：一趟扫描，每步字典操作 `O(1)`；空间 `O(min(n, k))`：字典里至多 `k` 个余数。

**写法要点。**
- `Counter({0: 1})` 一步给出带空前缀的初始计数；读取不存在的键返回 `0` 且**不会插入**，所以 `ans += seen[prefix]` 可以直接写，不用 `.get(prefix, 0)`。
- 每步取模，`prefix` 始终在 `[0, k)`，数值不膨胀；Python 的 `%` 对负被除数也给非负结果，不需要 `(x % k + k) % k`。
- 先 `ans += seen[prefix]`，再 `seen[prefix] += 1`：顺序不能反，否则把当前前缀自己也算成了“前面的前缀”。
- `prefix = ans = 0` 链式赋值两个不可变整数，互不影响。
- 想一行写出：`sum(c * (c - 1) // 2 for c in Counter(mods).values())`，`mods` 是含 `0` 的前缀余数列表，同一余数的 `c` 个前缀两两配对。

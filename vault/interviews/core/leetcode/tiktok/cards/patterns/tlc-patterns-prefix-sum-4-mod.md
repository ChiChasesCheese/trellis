---
id: tlc-patterns-prefix-sum-4-mod
node: patterns.prefix-sum
type: qa
step: 4
---
## Q
**前缀和与差分（Prefix Sum）｜和可被 `k` 整除与恰好 `k` 个奇数**

LC 974「和可被 K 整除的子数组」为什么用前缀和对 `k` 取模当键？LC 1248 把「奇数」映射成什么？

## A
`(pre[j] - pre[i]) % k == 0` ⇔ `pre[j] % k == pre[i] % k`。所以同余的前缀和可以两两配对。

```python
from collections import Counter
def sub_div_k(nums: list[int], k: int) -> int:
    cnt = Counter({0: 1})
    pre = ans = 0
    for x in nums:
        pre = (pre + x) % k           # Python 的 % 对负数也得 0..k-1
        ans += cnt[pre]
        cnt[pre] += 1
    return ans
print(sub_div_k([4, 5, 0, -2, -3, 1], 5), sub_div_k([5], 9))   # 7 0
```

- 关键在 `%`：Python 里 `-7 % 5 == 3`（结果与除数同号），不需要像 C++ / Java 那样补 `(pre % k + k) % k`。如果用了 `math.fmod(-7, 5)` 得到 `-2.0`，余数 3 和 -2 被当成两个不同的键，会漏掉配对。
- `nums` 含负数，所以必须用「前缀和 + 哈希」，不是滑动窗口。

**LC 1248**：把每个数映射成 `x & 1`（奇数为 1），问题就变成「和恰好等于 `k` 的子数组个数」，与 LC 560 完全一样：

```python
def nice(nums: list[int], k: int) -> int:
    cnt = Counter({0: 1})
    odd = ans = 0
    for x in nums:
        odd += x & 1                  # 到当前为止奇数的个数
        ans += cnt[odd - k]
        cnt[odd] += 1
    return ans
print(nice([1, 1, 2, 1, 1], 3), nice([2, 4, 6], 1), nice([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2))   # 2 0 16
```

识别规律：**把条件映射成 0/1 或同余类，再套前缀和 + 哈希**。

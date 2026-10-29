---
id: tlc-minimum-moves-to-make-array-complementary-2-code
node: b.minimum-moves-to-make-array-complementary
type: qa
step: 2
---
## Q
**LC 1674 使数组互补的最少操作次数**｜写出 Python 实现

偶数长度数组 `nums`（`2 ~ 10^5`，元素 `1 ~ limit`，`limit <= 10^5`）。每次操作把一个元素改成 `[1, limit]` 里的整数。使每对 `(nums[i], nums[n-1-i])` 的和都相等，最少需要几次操作？要求 `O(n + limit)`。

## A
**思路。** 对每个目标和 `s`，把所有对的代价加起来。每对的代价是分段常数：默认 `2`，在 `[lo+1, hi+limit]` 内降为 `1`，在 `s = a+b` 一点降为 `0`。用差分数组记录这些分段边界的增减，`itertools.accumulate` 做前缀和得到每个 `s` 的总代价，最后在合法范围 `2..2*limit` 内取最小。

```python
def min_moves(nums: list[int], limit: int) -> int:
    n = len(nums)
    diff = [0] * (2 * limit + 2)                 # diff[s]：目标和 s 的总操作数相对 s-1 的变化量
    for a, b in zip(nums[: n // 2], reversed(nums[n // 2 :])):   # 配对 (nums[i], nums[n-1-i])
        lo, hi = min(a, b), max(a, b)
        diff[2] += 2                             # 默认：每一对都要改 2 个数（s 从 2 开始）
        diff[lo + 1] -= 1                        # s 落在 [lo+1, hi+limit]：改 1 个数就够
        diff[hi + limit + 1] += 1
        diff[a + b] -= 1                         # s == a+b：不用改
        diff[a + b + 1] += 1
    cost = accumulate(diff)                      # cost[s] = 把所有对都变成和 s 的总操作数
    return min(c for s, c in enumerate(cost) if 2 <= s <= 2 * limit)
```

运行：`[1,2,4,3], limit=4` → `1`，`[1,2,2,1], limit=2` → `2`，`[1,2,1,2], limit=2` → `0`，`[1,1], limit=1` → `0`，`[1,1], limit=5` → `0`，`[1,5], limit=5` → `0`。

**复杂度。** 时间 `O(n + limit)`：处理 `n/2` 对各 `O(1)` 个端点，前缀和与取最小各扫 `2 * limit` 个位置；空间 `O(limit)`（差分数组）。

**写法要点。** `zip(nums[: n // 2], reversed(nums[n // 2 :]))` 一次取出所有对称对，不用手写 `nums[i]`、`nums[n-1-i]` 下标。`accumulate(diff)` 是前缀和的标准写法，返回迭代器，一次遍历不占额外空间。差分数组的写法统一是「区间 `[l, r]` 加 `v`：`diff[l] += v; diff[r + 1] -= v`」，「默认 `2`」从 `s = 2` 起一直延续到末尾，只在 `diff[2]` 记一笔就够，不必在末尾补减。`min(生成器)` 配合 `enumerate` 过滤出合法的 `s` 范围。

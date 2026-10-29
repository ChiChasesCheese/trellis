---
id: tlc-contiguous-array-2-code
node: b.contiguous-array
type: qa
step: 2
---
## Q
**LC 525 连续数组**｜写出 Python 实现

二进制数组 `nums`（长度 `1..10^5`，元素是 0 或 1）里，0 和 1 个数相等的最长连续子数组有多长？要求 `O(n)`。

## A
**思路。** 把 0 当 -1 做前缀和 `bal`。两个位置的 `bal` 相等，说明它们之间的子数组 0、1 一样多。字典记录每个 `bal` 第一次出现的下标，空前缀记为 `-1`。

```python
def find_max_length(nums: list[int]) -> int:
    first: dict[int, int] = {0: -1}      # 前缀差值 -> 它第一次出现的下标；空前缀记在 -1
    best = bal = 0                       # bal = 前缀里 1 的个数减 0 的个数
    for i, x in enumerate(nums):
        bal += 1 if x else -1            # 把 0 看成 -1
        if bal in first:                 # 两个前缀差值相同：中间那段 0 和 1 一样多
            best = max(best, i - first[bal])
        else:
            first[bal] = i               # 只记第一次出现，子数组才最长
    return best
```

运行：`[0,1]` → `2`，`[0,1,0]` → `2`，`[0,1,1,1,1,1,0,0,0]` → `6`，`[1]` → `0`，`[0,1,0,1]` → `4`。

**复杂度。** 时间 `O(n)`：一次遍历，每步一次字典查询；空间 `O(n)`：`bal` 最多有 `2n + 1` 种取值。

**写法要点。** `enumerate` 同时拿下标和值；`1 if x else -1` 用条件表达式完成 0 到 -1 的映射；`{0: -1}` 把「从开头起的子数组」并入同一条规则，不需要特判；`if/else` 而不是无条件赋值，保证只记最早下标。

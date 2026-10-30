---
id: tlc-house-robber-2-code
node: p2.house-robber
type: qa
step: 2
---
## Q
**LC 198 打家劫舍**｜写出 Python 实现

非负整数数组 `nums`（长度 `1` 到 `100`，每个元素 `0` 到 `400`）表示一排房屋的现金，相邻两间不能同时偷。返回不触发警报时能偷到的最大金额。要求 `O(n)` 时间、`O(1)` 空间。

## A
**思路。** 两个变量：`skip` 是“不偷当前房”时前面能得到的最大金额，`take` 是“偷当前房”时的最大金额。遍历每间房时同时更新：新 `skip` 取旧两者较大，新 `take` 是旧 `skip` 加当前现金。最后取两者较大。

```python
def rob(nums: list[int]) -> int:
    skip = take = 0                         # skip：不偷当前房的最优；take：偷当前房的最优
    for x in nums:
        skip, take = max(skip, take), skip + x
    return max(skip, take)
```

运行：`[1,2,3,1]` → `4`，`[2,7,9,3,1]` → `12`，`[5]` → `5`，`[2,1,1,2]` → `4`，`[0]` → `0`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`。

**写法要点。**
- `skip, take = max(skip, take), skip + x`：元组赋值先算完右边两个值再同时赋值，右边的 `skip` 都是旧值，不用临时变量，也避免了“先改一个再用它”的顺序错误。
- 用 `skip = take = 0` 起步，让空前缀自然成立，不需要为长度 `1` 或 `2` 单独写边界。
- 经典等价写法是 `prev, cur = cur, max(cur, prev + x)`：`cur` 是到目前为止的最优，`prev` 是再前一格的最优，同样两个变量。
- 只要结果不需要路径，就别开 `dp` 数组；需要路径时再保留数组回溯。

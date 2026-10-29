---
id: tlc-number-of-longest-increasing-subsequence-2-code
node: b.number-of-longest-increasing-subsequence
type: qa
step: 2
---
## Q
**LC 673 最长递增子序列的个数**｜写出 Python 实现

未排序整数数组 `nums`（`1 <= nums.length <= 2000`，`-10^6 <= nums[i] <= 10^6`），返回最长**严格**递增子序列的个数。

## A
**思路。** `length[i]` 记以 `nums[i]` 结尾的最长长度，`count[i]` 记达到该长度的个数。对每个 `j < i` 且 `nums[j] < nums[i]`：`length[j] + 1` 更大就覆盖，相等就累加。最后对所有达到最大长度的位置求和。

```python
def find_number_of_lis(nums: list[int]) -> int:
    n = len(nums)
    length = [1] * n                 # length[i]：以 nums[i] 结尾的最长递增子序列长度
    count = [1] * n                  # count[i]：达到这个长度的子序列个数
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:        # 找到更长的：计数改成 j 的计数
                    length[i], count[i] = length[j] + 1, count[j]
                elif length[j] + 1 == length[i]:     # 一样长的另一种来源：累加
                    count[i] += count[j]
    longest = max(length)
    return sum(c for l, c in zip(length, count) if l == longest)
```

运行：`[1,3,5,4,7]` → `2`，`[2,2,2,2,2]` → `5`，`[1]` → `1`，`[1,2,3,4,5]` → `1`，`[5,4,3,2,1]` → `5`。

**复杂度。** 时间 `O(n^2)`：外层 `n`、内层至多 `n`；空间 `O(n)`。

**写法要点。** `length[i], count[i] = length[j] + 1, count[j]` 用元组同时赋值，不会因为先改 `length[i]` 而影响右边；`zip(length, count)` 并排遍历两个数组，`sum(生成器)` 一次完成筛选与求和；先 `longest = max(length)` 存下来，生成器里就不会每次重算。

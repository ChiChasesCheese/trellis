---
id: tlc-summary-ranges-2-code
node: b.summary-ranges
type: qa
step: 2
---
## Q
**LC 228 汇总区间**｜写出 Python 实现

升序、无重复的整数数组 `nums`（`0 <= nums.length <= 20`，元素范围 `-2^31` 到 `2^31 - 1`），返回恰好覆盖所有数字的最小有序区间字符串列表：单个数写 `"a"`，多个写 `"a->b"`。

## A
**思路。** `i` 指向当前段首，`j` 从 `i` 出发，只要下一个数等于当前数加一就继续右移；`[i, j]` 就是一个极长连续段。按 `i == j` 与否格式化，然后让 `i = j + 1` 开始下一段。

```python
def summary_ranges(nums: list[int]) -> list[str]:
    ans: list[str] = []
    i = 0
    while i < len(nums):
        j = i                                          # [i, j] 是当前连续段
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        ans.append(str(nums[i]) if i == j else f"{nums[i]}->{nums[j]}")
        i = j + 1                                      # 下一段从 j + 1 开始
    return ans
```

运行：`[0,1,2,4,5,7]` → `['0->2', '4->5', '7']`；`[0,2,3,4,6,8,9]` → `['0', '2->4', '6', '8->9']`；`[]` → `[]`；`[5]` → `['5']`；`[-2147483648, 2147483647]` → `['-2147483648', '2147483647']`。

**复杂度。** 时间 `O(n)`：内层循环推进的 `j` 之后不会再被外层重复访问；额外空间 `O(1)`，输出不计。

**写法要点。** f-string `f"{nums[i]}->{nums[j]}"` 比 `str(a) + "->" + str(b)` 短且不会漏掉 `str`；条件表达式 `A if i == j else B` 把「单点 / 多点」两种格式放在一行里；`j + 1 < len(nums)` 放在 `and` 左侧，利用短路避免越界。

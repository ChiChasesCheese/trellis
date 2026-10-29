---
id: tlc-tt-pythagorean-triple-in-array-2-code
node: b.tt-pythagorean-triple-in-array
type: qa
step: 2
---
## Q
**整数数组中的勾股三元组**｜写出 Python 实现

整数数组 `nums`（`0 <= n <= 3000`，`|nums[i]| <= 10^5`，可含负数、`0`、重复值）。判断是否存在三个不同下标 `i`、`j`、`k`，使 `nums[i]^2 + nums[j]^2 == nums[k]^2`，返回布尔值，时间 `O(n^2)`。

## A
**思路。** 把每个数换成平方并排序。从最大的位置往小枚举斜边 `k`，用左右指针在 `[0, k - 1]` 里找两个平方数之和等于 `sq[k]`：和小就移左指针，和大就移右指针。

```python
def has_pythagorean_triple(nums: list[int]) -> bool:
    sq = sorted(x * x for x in nums)             # 平方抹掉符号；排序后位置不同的元素仍占不同下标
    for k in range(len(sq) - 1, 1, -1):          # sq[k] 当斜边，直角边从更小的下标里找
        i, j = 0, k - 1
        while i < j:
            s = sq[i] + sq[j]
            if s == sq[k]:
                return True
            if s < sq[k]:
                i += 1
            else:
                j -= 1
    return False
```

运行：`[3,4,5]` → `True`；`[-3,4,-5]` → `True`；`[0,0,0]` → `True`；`[0,5,-5]` → `True`；`[0,5]` → `False`；`[1,2,3]` → `False`；`[5,12,13,1]` → `True`；`[3,3,5]` → `False`；`[]` → `False`；`[6,8,10,7]` → `True`。

**复杂度。** 时间 `O(n^2)`；空间 `O(n)`。

**写法要点。** `sorted(x * x for x in nums)` 用生成器一步完成「平方 + 排序」，原数组不变；`range(len(sq) - 1, 1, -1)` 的下界 `1` 保证 `k` 左边至少有两个元素；`i < j` 而不是 `i <= j`，两条直角边必须是不同下标；Python 整数不溢出，`10^5` 的平方 `10^10` 也不需要特殊处理（C++ / Java 里要用 `long`）；不要用 `set` 去重，会丢掉值相同、下标不同的合法组合。

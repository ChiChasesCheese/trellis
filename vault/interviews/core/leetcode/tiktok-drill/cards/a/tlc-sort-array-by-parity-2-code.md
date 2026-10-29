---
id: tlc-sort-array-by-parity-2-code
node: a.sort-array-by-parity
type: qa
step: 2
---
## Q
**LC 905 按奇偶排序数组**｜写出 Python 实现

数组 `nums`（`1 <= 长度 <= 5000`，`0 <= nums[i] <= 5000`）：原地把偶数放前面、奇数放后面，返回任一满足条件的数组。要求 `O(n)` 时间、`O(1)` 额外空间。

## A
**思路。** 两个指针从两端相向走：左边是偶数就右移，右边是奇数就左移，否则就是「左奇右偶」，交换后两端各进一步。

```python
def sort_array_by_parity(nums: list[int]) -> list[int]:
    left, right = 0, len(nums) - 1
    while left < right:
        if nums[left] % 2 == 0:            # 左边已经是偶数：放行
            left += 1
        elif nums[right] % 2 == 1:         # 右边已经是奇数：放行
            right -= 1
        else:                              # 左奇右偶：交换，两端各前进一步
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
    return nums
```

运行：`[3,1,2,4]` → `[4, 2, 1, 3]`，`[0]` → `[0]`，`[1]` → `[1]`，`[1,3,5]` → `[1, 3, 5]`，`[2,4]` → `[2, 4]`。

**复杂度。** 时间 `O(n)`：每轮至少一个指针向中间移动一步；额外空间 `O(1)`。

**写法要点。** `a, b = b, a` 是 Python 的交换写法，右侧先打包成元组再解包，不需要临时变量；`if / elif / else` 三分支让每轮只做一件事，循环不变量一目了然；偶数判断也可写 `x & 1 == 0`：Python 里位运算 `&` 的优先级高于比较 `==`，等价于 `(x & 1) == 0`；C / Java 里恰好相反，必须加括号，所以跨语言时 `% 2` 更不容易写错。

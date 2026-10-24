---
id: tlc-single-element-in-a-sorted-array-4-followup
node: a.single-element-in-a-sorted-array
type: qa
step: 4
---
## Q
**LC 540 有序数组中的单一元素**｜追问

面试官接着问：（1）数组没有排序了（LC 136）？（2）其他元素出现三次、只有一个出现一次（LC 137）？（3）能不能不对齐 `mid`，写得更短？

## A
1. **无序。** 相同的数异或为 `0`，任何数异或 `0` 是自身，所以全体异或剩下的就是单一元素，`O(n)` 时间、`O(1)` 空间：`reduce(xor, nums)`。`[4,1,2,1,2]` → `4`。有序时二分更快，无序时异或最优。
2. **其余出现三次（LC 137）。** 对每个二进制位统计所有数在该位上 `1` 的个数，模 `3`，余数就是单一元素在该位的值；32 位上各做一遍，`O(32n)`。注意 Python 的负数是无限位补码，要自己把第 31 位当符号位处理。
3. **不对齐的写法。** 用 `mid ^ 1` 取同一对里的另一个下标：
```python
def single_non_duplicate_xor(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] == nums[mid ^ 1]:      # mid 偶数时配 mid+1，奇数时配 mid-1
            lo = mid + 1                    # 这一对完整：单一元素在右边
        else:
            hi = mid
    return nums[lo]
```
`[1,1,2,3,3,4,4,8,8]` → `2`，`[3,3,7,7,10,11,11]` → `10`。`mid` 偶数时与 `mid + 1` 比，奇数时与 `mid - 1` 比，两种情况都表示“mid 所在的这一对完整”，所以 `lo = mid + 1` 之后 `lo` 可能是奇数，但下一轮 `mid ^ 1` 仍能正确配对。

**Python 提醒**：Python 里按位运算符（`&`、`^`、`|`）的优先级高于比较运算符，`mid ^ 1 == x` 等于 `(mid ^ 1) == x`；C / Java 正相反，`==` 比 `^`、`&` 优先级高，同样的写法必须加括号。从其他语言搬过来的位运算习惯，在 Python 里不必多加括号，但也别误以为两边行为一致。

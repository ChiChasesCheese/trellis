---
id: tlc-product-of-array-except-self-4-followup
node: a.product-of-array-except-self
type: qa
step: 4
---
## Q
**LC 238 除了自身以外数组的乘积**｜追问

面试官接着问：（1）如果允许除法，怎么处理数组里的 `0`？（2）不想改写输出数组，能不能写得更声明式一点？（3）如果要求「除自身外的**和**」呢？分别怎么改。

## A
1. **允许除法**：先数零的个数。`>= 2` 个零，全部答案为 `0`；恰好 `1` 个零，只有零所在位置等于其余非零数之积，其余位置为 `0`；没有零，`total // x`。一趟求积、一趟填答案，`O(n)`。
2. **声明式写法**：用 `accumulate` 与 `operator.mul` 分别算前缀积和后缀积，再 `zip` 相乘：

```python
from itertools import accumulate
from operator import mul

def product_prefix_suffix(nums: list[int]) -> list[int]:
    pre = [1, *accumulate(nums[:-1], mul)]                    # pre[i] = nums[0..i-1] 之积
    suf = [*accumulate(reversed(nums[1:]), mul)][::-1] + [1]  # suf[i] = nums[i+1..] 之积
    return [a * b for a, b in zip(pre, suf)]
```

   `[1,2,3,4]` → `[24, 12, 8, 6]`。可读性好，但多用 `O(n)` 额外空间，进阶要求 `O(1)` 时仍用两趟滚动变量版。
3. **除自身外的和**：`total - nums[i]`，不需要前后缀；乘法没有「逆运算」才要前后缀分解，加法可以直接减。

**Python 提醒**：`accumulate(iterable, func)` 的第一个输出是第一个元素本身，不会自动补初值；要得到「不含自己」的前缀，需要像上面那样把初值 `1` 放在最前面并对 `nums[:-1]` 累计。

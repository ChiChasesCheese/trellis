---
id: uth-java-sort-3-timsort-contract
node: java.sort
type: qa
step: 3
---
## Q
**Comparator 写错会怎样**｜Java · OpenJDK 25

用 `(p, q) -> p - q` 当比较器排序 `Integer`，为什么可能排错？TimSort 还会抛出什么异常？

## A
**背景。** 对象排序靠你写的比较器：返回负数表示 p 在前，正数表示 q 在前。归并时的每一步判断都假设比较结果自洽（p<q 且 q<r 则 p<r）；写错了，算法就没法保证结果。

**结构。** Java 的 `TimSort` 做法和 Python 一致：找 run、二分插入补到 `minrun`、按栈规则归并；`minrun` 在 16 到 32 之间（Python 是 32 到 64）。

**细节。**

- 实测 10 万个元素的比较次数：有序 99999，倒序 99999，随机约 153 万。
- `p - q` 在 `MAX_VALUE` 与负数相减时溢出（结果超出 int 范围，变成相反的符号），实测 `[MAX, -5, 3, MIN, 0]` 排成 `[MAX, -5, 0, 3, MIN]`。
- 比较结果前后矛盾（实测用随机数）时，可能抛 `IllegalArgumentException: Comparison method violates its general contract!`。

**为什么。** 归并依赖比较结果可传递；违反它，算法的不变式就被破坏。

**坑。** 用 `Integer.compare(p, q)` 或 `Comparator.comparingInt`。

**例题：** LC 179 最大数

给一组非负整数，把它们首尾拼接，使拼出的数字最大，返回字符串。例：`[3,30,34,5,9]` 得 `"9534330"`。

```python
from functools import cmp_to_key

def largest_number(nums: list[int]) -> str:
    def compare(a: str, b: str) -> int:
        return (b + a > a + b) - (b + a < a + b)     # a+b 更大时 a 排前面，返回负数

    strs = sorted(map(str, nums), key=cmp_to_key(compare))
    return "0" if strs[0] == "0" else "".join(strs)  # 最大的是 0，说明全是 0
```

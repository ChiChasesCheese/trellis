---
id: tlc-single-number-iii-2-code
node: a.single-number-iii
type: qa
step: 2
---
## Q
**LC 260 只出现一次的数字 III**｜写出 Python 实现

整数数组 `nums`（长度 `2..3 * 10^4`，元素在 `[-2^31, 2^31 - 1]`）里恰有两个元素只出现一次，其余各出现两次，返回这两个元素（任意顺序），线性时间、常数空间。

## A
**思路。** 全部异或得 `both = a ^ b`。取 `both` 的最低位 1 作为分组依据，`a`、`b` 在这位不同。再扫一遍，只异或这一位为 1 的元素，得到其中一个落单数 `a`，另一个是 `both ^ a`。

```python
def single_number_iii(nums: list[int]) -> list[int]:
    both = 0
    for x in nums:
        both ^= x                                    # both == a ^ b，且 a != b 所以 both != 0
    low = both & -both                               # 最低位的 1：a、b 在这一位不同
    a = 0
    for x in nums:
        if x & low:                                  # 只异或这一位为 1 的那一组
            a ^= x
    return [a, both ^ a]                             # 另一个由 a ^ b ^ a 得到，不用再扫一遍
```

运行：`[1,2,1,3,2,5]` → `[3, 5]`，`[-1,0]` → `[-1, 0]`，`[0,1]` → `[1, 0]`，`[-2**31, 2**31-1]` → `[2147483647, -2147483648]`。

**复杂度。** 时间 `O(n)`，扫两遍；空间 `O(1)`。

**写法要点。** `x & -x` 取最低位的 1（补码里 `-x = ~x + 1`），Python 对负数也成立；只维护一个累加器 `a`，第二个数用 `both ^ a` 推出，少一个变量也少一遍扫描；返回值用 `list[int]`，顺序任意。

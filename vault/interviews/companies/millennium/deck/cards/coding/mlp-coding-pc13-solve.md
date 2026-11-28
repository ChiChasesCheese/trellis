---
id: mlp-coding-pc13-solve
node: coding.pc13
step: 1
type: qa
---
## Q
**能否重排成 8 的倍数：题与解**｜编程轮

给一个由数字字符组成的字符串 `s`，问能不能把这些数字重新排列，得到一个能被 8 整除的数。例如 `"123"` 可以（排成 312，等于 8×39），`"111"` 不行。

## A
**一句话思路。** 1000 是 8 的倍数，所以一个数能不能被 8 整除，只取决于末三位。于是只要问：手里的数字够不能拼出某个三位的 8 的倍数（000、008、016……992，共 125 个），其余数字排在前面不影响结果。不用枚举全部排列。位数不足三位时直接试所有排列。这里允许前导零，如果题目不允许，要先向面试官问清。

```python
from collections import Counter
from itertools import permutations

def can_make_multiple_of_8(s):
    if len(s) < 3:                             # 不足三位：直接试所有排列
        return any(int("".join(p)) % 8 == 0 for p in permutations(s))
    cnt = Counter(s)
    for k in range(0, 1000, 8):                # 末三位只能是 000、008、016 … 992
        need = Counter(f"{k:03d}")
        if all(cnt[d] >= c for d, c in need.items()):   # 手里的数字够拼这三位
            return True                        # 其余数字排在前面，不影响整除
    return False

assert can_make_multiple_of_8("123")           # 312 = 8 * 39
assert not can_make_multiple_of_8("111")
assert can_make_multiple_of_8("16") and not can_make_multiple_of_8("17")
assert can_make_multiple_of_8("0")
assert not can_make_multiple_of_8("100")       # 001、010、100 都不是 8 的倍数
```

**复杂度。** 125 个候选，每个比较至多 3 种数字，再加一次计数，所以是 O(n)，空间 O(1)；暴力枚举全部排列是 O(n!)。

**边写边讲。**
- "Since **1000 is divisible by 8**, only the **last three digits** decide divisibility."
- "So I count the digits and check whether I can spell any of the **125 three-digit multiples of 8**."
- "Strings shorter than three digits I just brute-force; I'll also confirm whether **leading zeros** are allowed."

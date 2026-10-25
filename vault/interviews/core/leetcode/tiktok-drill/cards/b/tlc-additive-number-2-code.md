---
id: tlc-additive-number-2-code
node: b.additive-number
type: qa
step: 2
---
## Q
**LC 306 累加数**｜写出 Python 实现

只含数字字符的字符串 `num`（长度 `1` 到 `35`）。判断能否切成至少三个数，使除开头两个数外每个数都等于前两个数之和；多位数不能有前导零（单独的 `0` 允许）。返回布尔值。

## A
**思路。** 枚举第一个数 `num[:i]` 和第二个数 `num[i:j]`。先排除前导零，再把两数转成 `int`；之后反复 `a, b = b, a + b`，要求 `str(b)` 正好出现在 `num` 当前位置，推进位置；走到末尾恰好用完就成功。

```python
def is_additive_number(num: str) -> bool:
    n = len(num)

    def valid(i: int, j: int) -> bool:     # 前两个数是 num[:i] 和 num[i:j]，其后每个数都被唯一确定
        if (i > 1 and num[0] == "0") or (j - i > 1 and num[i] == "0"):
            return False                   # 多位数不能有前导 0
        a, b = int(num[:i]), int(num[i:j])
        k = j
        while k < n:
            a, b = b, a + b
            s = str(b)
            if not num.startswith(s, k):   # 下一个数必须正好是 a + b
                return False
            k += len(s)
        return True                        # k == n：恰好用完

    return any(
        valid(i, j)
        for i in range(1, n)
        for j in range(i + 1, n)           # j < n：保证至少还有第三个数
        if max(i, j - i) <= n - j          # 第三个数的位数不会比两个加数的较长者短
    )
```

运行：`"112358"` → `True`，`"199100199"` → `True`，`"000"` → `True`，`"101"` → `True`，`"1023"` → `False`，`"12"` → `False`，`"1"` → `False`。

**复杂度。** 时间 `O(n^3)`：`(i, j)` 共 `O(n^2)` 对，每对的校验最多 `O(n)` 个数且每个数的加法和比较是 `O(n)`；实际由于剪枝和提前失败，远小于上界。空间 `O(n)`。

**写法要点。** `str.startswith(s, k)` 带起始位置参数，不用切片 `num[k:k+len(s)] == s`，省掉一次切片复制；`any(生成器)` 在第一个成功的 `(i, j)` 处短路；元组交换 `a, b = b, a + b` 一步完成滚动；大整数由 Python 的 `int` 自动支持，不用手写字符串加法；把 `if` 过滤放进生成器末尾，让不可能的 `(i, j)` 不进入 `valid`。

---
slug: additive-number
---
## Q
**LC 306 累加数**｜Medium

判断数字串 `num` 能否拆成至少 3 个数的累加序列：除前两个数外，每个数等于前两数之和；多位数不能有前导 `0`。

## A
**一句话。** 枚举前两个数的切分点，之后每个数都被唯一确定，逐个核对是否接得上。

```python
def is_additive_number(num):
    n = len(num)

    def valid(i, j):           # 前两个数 num[:i]、num[i:j]
        if (i > 1 and num[0] == "0") or \
           (j - i > 1 and num[i] == "0"):
            return False       # 多位数不能前导 0
        a, b = int(num[:i]), int(num[i:j])
        k = j
        while k < n:
            a, b = b, a + b
            s = str(b)
            if not num.startswith(s, k):
                return False
            k += len(s)
        return True

    return any(valid(i, j) for i in range(1, n)
               for j in range(i + 1, n))
```

**复杂度。** 时间 `O(n^3)`，空间 `O(n)`。

**易错点。**
- 漏查前导零：`"1023"` 会被当成 `1, 02, 3` 而返回 `True`。
- `j` 取到 `n`：`"12"` 只有两个数却返回 `True`，`j` 必须小于 `n`。

**追问。**
- 数字很大会溢出吗？：Python 不会；Java / C++ 用字符串竖式加法。
- 要返回具体序列（LC 842）？：校验时把每个数收集进列表，并限制不超过 `2^31 - 1`。

**同模式。** LC 842 将数组拆分成斐波那契序列、LC 93 复原 IP 地址、LC 282 给表达式添加运算符、LC 131 分割回文串

---
slug: maximum-lcci
---
## Q
**面试题 16.07 最大数值**｜Easy

返回两个整数 `a`、`b` 中较大的，不得使用 if-else、比较运算符或 `max`。

## A
**一句话。** 比大小就是看 `a-b` 的符号位，用位运算取出 `neg`，答案 `a - neg*(a-b)`。

```python
def maximum(a, b):
    diff = a - b
    neg = (diff >> diff.bit_length()) & 1   # a < b 时为 1
    return a - neg * diff
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 把符号位写死成 `>> 31`：`|a-b| >= 2^31` 时判错，`maximum(2147483647, -1)` 得 `-1`。
- 写成 `a*(a>b) + b*(a<=b)`：用了比较运算符，违反题意。

**追问。**
- 最小值怎么求？：`a + b - maximum(a, b)`。
- C++/Java 里 `a-b` 溢出怎么办？：先转 `long`，或分别取符号位，同号用差、异号看符号。

**同模式。** LC 371 两整数之和、LC 29 两数相除、LC 136 只出现一次的数字

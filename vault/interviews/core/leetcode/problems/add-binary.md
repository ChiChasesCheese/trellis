---
slug: add-binary
---
## Q
**LC 67 二进制求和（Add Binary）**｜Easy

给两个二进制字符串 `a`、`b`，以二进制字符串返回它们的和。

## A
**一句话。** 双指针从末尾逐位相加带进位，`divmod(total, 2)` 拆出进位和当前位。

```python
def add_binary(a, b):
    i, j, carry = len(a) - 1, len(b) - 1, 0
    out = []                       # 从低位到高位产出
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += int(a[i])
            i -= 1
        if j >= 0:
            total += int(b[j])
            j -= 1
        carry, bit = divmod(total, 2)
        out.append(str(bit))
    return "".join(reversed(out))
```

**复杂度。** 时间 `O(max(m, n))`，空间 `O(max(m, n))`。

**易错点。**
- 循环条件漏掉 `or carry`：`("11", "1")` 得 `"00"`，应为 `"100"`。
- 忘记反转：结果是低位在前，`("11", "1")` 得 `"001"`。

**追问。**
- 为什么不能直接 `int(a, 2)` 相加？：Java / C++ 里长度 `10^4` 超出 64 位，必须逐位处理。

**同模式。** LC 66 加一、LC 2 两数相加、LC 415 字符串相加、LC 43 字符串相乘

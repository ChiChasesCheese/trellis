---
slug: multiply-strings
---
## Q
**LC 43 字符串相乘**｜Medium

两个字符串表示的非负整数 `num1`、`num2`，返回乘积字符串，不能用大整数库或直接转整数。

## A
**一句话。** 竖式乘法，`a[i]*b[j]` 落在第 `i+j` 位，先累加不进位，最后统一进位。

```python
def multiply(num1, num2):
    a = [int(c) for c in reversed(num1)]   # 个位在下标 0
    b = [int(c) for c in reversed(num2)]
    res = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i + j] += x * y
    carry = 0
    for k in range(len(res)):
        carry, res[k] = divmod(res[k] + carry, 10)
    while len(res) > 1 and res[-1] == 0:   # 去前导零，留一个 0
        res.pop()
    return "".join(map(str, reversed(res)))
```

**复杂度。** 时间 `O(mn)`，空间 `O(m+n)`。

**易错点。**
- 忘了去前导零：`("2","3")` 得 `"06"`，`("0","5")` 得 `"00"`。
- 下标方向混用：反转后位权是 `i+j`，原序则是 `i+j+1`，容易错一位。

**追问。**
- 字符串相加怎么写？：同样从低位进位，`zip_longest` 对齐不等长（LC 415）。
- 能更快吗？：Karatsuba 分治 `O(n^1.58)`，面试一般不要求。

**同模式。** LC 415 字符串相加、LC 67 二进制求和、LC 2 两数相加、LC 66 加一

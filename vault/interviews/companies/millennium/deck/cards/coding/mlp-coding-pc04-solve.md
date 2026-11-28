---
id: mlp-coding-pc04-solve
node: coding.pc04
step: 1
type: qa
---
## Q
**字符串大数加法：题与解**｜编程轮

两个非负整数以十进制字符串给出，返回它们的和（字符串）。不许用 `int()` 把整串转成数字。进阶：数字可以带 `+` 或 `-` 号，要同时支持减法。

## A
**一句话思路。** 把小学竖式搬进代码：两个指针从最低位往左走，每一位加上进位，`divmod(和, 10)` 得到本位和新进位；位数用完了且进位为 0 才停。带符号时，同号就数量级相加、符号不变；异号就用大的数量级减小的，符号跟大的那个；减法等于加上对方的相反数。

```python
def add_unsigned(a, b):
    if not a or not b or not (a + b).isdigit():
        raise ValueError("bad operand")              # 空串、非数字字符都非法
    i, j, carry, out = len(a) - 1, len(b) - 1, 0, []
    while i >= 0 or j >= 0 or carry:                 # 最后可能还剩一个进位，如 999 + 1
        da = ord(a[i]) - 48 if i >= 0 else 0         # 单个字符转数字，不对整串用 int()
        db = ord(b[j]) - 48 if j >= 0 else 0
        carry, digit = divmod(da + db + carry, 10)
        out.append(chr(48 + digit))
        i -= 1
        j -= 1
    return strip("".join(reversed(out)))

def strip(s):                                        # 去前导零，但保留单个 "0"
    k = 0
    while k < len(s) - 1 and s[k] == "0":
        k += 1
    return s[k:]

def cmp_mag(a, b):                                   # 比较两个数量级：先比长度，再逐字典序
    a, b = strip(a), strip(b)
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    return (a > b) - (a < b)

def sub_mag(a, b):                                   # 要求 a >= b，从低位借位
    a, b = strip(a), strip(b)
    i, j, borrow, out = len(a) - 1, len(b) - 1, 0, []
    while i >= 0:
        d = ord(a[i]) - 48 - (ord(b[j]) - 48 if j >= 0 else 0) - borrow
        borrow = 1 if d < 0 else 0
        out.append(chr(48 + d + 10 * borrow))
        i -= 1
        j -= 1
    return strip("".join(reversed(out)))

def split_sign(s):
    if not s:
        raise ValueError("empty")
    neg = s[0] == "-"
    mag = s[1:] if s[0] in "+-" else s
    if not mag or not mag.isdigit():
        raise ValueError("bad operand")
    return neg, strip(mag)

def add_signed(a, b):
    na, ma = split_sign(a)
    nb, mb = split_sign(b)
    if na == nb:
        r = add_unsigned(ma, mb)
        neg = na
    else:
        c = cmp_mag(ma, mb)
        if c == 0:
            return "0"                               # 零永远不带符号
        r = sub_mag(ma, mb) if c > 0 else sub_mag(mb, ma)
        neg = na if c > 0 else nb                    # 符号跟数量级大的一方
    return "-" + r if neg and r != "0" else r

def subtract_signed(a, b):
    return add_signed(a, b[1:] if b.startswith("-") else "-" + b.lstrip("+"))

print(add_unsigned("999", "1"), add_unsigned("007", "013"))   # 1000 20
print(add_signed("-5", "3"), subtract_signed("5", "8"), add_signed("-0", "0"))   # -2 -3 0
```

**复杂度。** 加减 O(max(len a, len b)) 时间，O(位数) 空间。

**边写边讲。**
- "I walk both strings **from the right** with two pointers and a running carry, like adding on paper."
- "The loop runs while either string has digits **or a carry remains**, so `999 + 1` works."
- "Subtraction is **add the negation**, so I reuse one add and one compare helper."

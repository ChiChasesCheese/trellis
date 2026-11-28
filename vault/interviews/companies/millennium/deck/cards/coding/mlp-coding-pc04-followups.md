---
id: mlp-coding-pc04-followups
node: coding.pc04
step: 2
type: qa
---
## Q
**字符串大数运算：追问与变体**｜编程轮

字符串加法写完后，面试官会往哪些方向追问？

## A
- **乘法：** 竖式长乘法，用一个长度 len(a)+len(b) 的数组累加，`acc[i+j]` 存第 i 位乘第 j 位的贡献；每一行乘完后，残留进位要写到更高一位。时间 O(n·m)，因为结果本身就有 n+m 位，不可能压到线性；要更快可以提 Karatsuba（分治，约 O(n^1.585)）。

```python
def multiply(a, b, base=10):
    da = [int(c, 36) for c in reversed(a)]       # 单个字符转数字，不对整串用 int
    db = [int(c, 36) for c in reversed(b)]
    acc = [0] * (len(da) + len(db))
    for i, x in enumerate(da):
        carry = 0
        for j, y in enumerate(db):
            t = acc[i + j] + x * y + carry
            acc[i + j], carry = t % base, t // base
        acc[i + len(db)] += carry                # 别忘了内层结束后的进位
    s = "".join("0123456789abcdefghijklmnopqrstuvwxyz"[d] for d in reversed(acc))
    return s.lstrip("0") or "0"
```

- **任意进制（2 到 36）：** 把 10 换成 `base`，数字用 `0-9a-z`；出现该进制下不存在的字符（如八进制里的 `8`）抛 `ValueError`。
- **符号规则：** 同号得正、异号得负，结果为零不带符号；输入 `-0` 也要归一成 `0`。
- **前导零：** 输入 `007` 要容忍，输出去掉前导零，但 `0` 本身保留。
- **为什么不直接 `int(a) + int(b)`：** Python 的大整数能算对，但面试要看的是手写进位、借位；先问清楚能不能用 `int`，不能就按竖式写。
- **用链表或数组做同一件事：** 数字倒序存放时，加法就是同步遍历两个序列加进位，和字符串版是同一种写法。
- **会多花一个测试用例的边界：** `999 + 1`（连续进位直到多出一位）；两个数长度不同；`5 - 8` 得 `-3`；`-5 - -8` 得 `3`；只有符号没有数字（`-`）和空串抛 `ValueError`；乘数有一个是 `0` 直接返回 `0`。

**英文答法。**
- "Multiplication is **O(n·m)**, since the product itself has about n plus m digits."
- "After the inner loop there can still be a **leftover carry**, so I write it to the next position."
- "I'd confirm whether I'm allowed to use `int()`; if not, I do the carries **by hand**."

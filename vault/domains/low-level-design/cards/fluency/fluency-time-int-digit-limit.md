---
id: fluency-time-int-digit-limit
node: fluency.time-numbers
type: qa
step: 8
---
## Q
接口收到金额字符串，代码是 `int(s)` 再检查 `<= 10**12`。攻击者传了一个 5000 位的数字串。Python 3.11 上会发生什么？Python 的整数没有溢出，为什么还要在解析前后设上界？

## A
**先限长度再 int()，上界按合同检查**

- **3.11 的位数上限**：`int(str)` 和 `str(int)` 在十进制位数超过 4300 时抛 `ValueError`（用来挡二次方复杂度的拒绝服务攻击）；这个限制随 3.11 引入，也回补进了 3.7 到 3.10 的后期安全版本，所以同一份代码在不同补丁版本上行为可能不同；
- **没捕获就是 500**：上限抛的是 `ValueError`，和“不是数字”一样；边界解析函数要捕获它，返回 400；
- **先检查长度更省**：金额最多 13 位，字符串超长直接拒绝，不要让几千位的数进入 `int()`；
- **`int` 无上限不等于不用检查**：另一端可能是 JavaScript（整数超过 2**53 失去精度）或数据库的 64 位整数（上界 2**63 - 1）；上界写成常量，并按合同决定含不含边界；
- **`int()` 也比想象的宽**：接受 `"1_000"`、前后空白、`"+5"`、全角数字；要“只收 ASCII 数字”就先 `s.isascii() and s.isdigit()`；
- **测试成对写**：恰好等于上界通过，上界加一被拒绝。

```python
MAX_CENTS = 10**12

def parse_cents(s: str) -> int:
    if not (s.isascii() and s.isdigit()) or len(s) > 13:   # 先挡格式和长度
        raise ValueError("invalid_amount")
    n = int(s)
    if not 1 <= n <= MAX_CENTS:                            # 上界含边界
        raise ValueError("invalid_amount")
    return n

try: int("9" * 5000)                      # 直接 int()：3.11 抛 ValueError
except ValueError as e: print(str(e)[:44])
print(parse_cents("1000000000000"))       # 恰好上界：通过
for s in ("1000000000001", "９９", "9" * 5000):
    try: parse_cents(s)
    except ValueError as e: print(e)      # 三个都是 invalid_amount
```

<details class="pt"><summary>延伸</summary>

`sys.set_int_max_str_digits()` 可以改上限，但服务面对不可信输入时不要调大；大数运算的时间随位数平方增长，上限本身就是保护。

</details>

**知识点：**时间与数字（Time & Numbers）

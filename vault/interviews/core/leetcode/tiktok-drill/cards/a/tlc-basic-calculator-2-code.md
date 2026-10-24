---
id: tlc-basic-calculator-2-code
node: a.basic-calculator
type: qa
step: 2
---
## Q
**LC 224 基本计算器**｜写出 Python 实现

字符串 `s`（长度 `1` 到 `3×10^5`）是由数字、`+`、`-`、`(`、`)` 和空格组成的有效表达式，`-` 可作一元负号。不使用 `eval()`，一遍扫描，返回表达式的值（所有中间值都在 32 位整数内）。

## A
**思路。** 变量 `res` 是当前括号层已结算的和，`num` 是正在读的数，`sign` 是下一个数的符号。遇到 `+`/`-` 先结算上一个数再改 `sign`；遇到 `(` 把 `(res, sign)` 压栈并重置；遇到 `)` 结算括号内最后一个数，再把括号结果乘上括号前的符号加回外层。

```python
def calculate(s: str) -> int:
    stack: list[tuple[int, int]] = []     # 进括号前保存 (已累计的结果, 括号前的符号)
    res, num, sign = 0, 0, 1
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch in "+-":
            res += sign * num             # 结算上一个数
            num, sign = 0, 1 if ch == "+" else -1
        elif ch == "(":
            stack.append((res, sign))     # 括号内从 0 重新算
            res, sign = 0, 1
        elif ch == ")":
            res += sign * num             # 结算括号里最后一个数
            num = 0
            prev_res, prev_sign = stack.pop()
            res = prev_res + prev_sign * res   # 括号结果乘上括号前的符号，再并回去
    return res + sign * num
```

运行：`"1 + 1"` → `2`，`" 2-1 + 2 "` → `3`，`"(1+(4+5+2)-3)+(6+8)"` → `23`，`"-(2+3)"` → `-5`，`"(-2)"` → `-2`，`"1-(-2)"` → `3`，`"2-(5-6)"` → `3`；`"(" * 100000 + "1" + ")" * 100000` → `1`。

**复杂度。** 时间 `O(n)`：每个字符一次常数操作；空间 `O(d)`，`d` 是括号嵌套深度。

**写法要点。** 栈里存元组 `(res, sign)`，弹出时直接解包；`num, sign = 0, 1 if ch == "+" else -1` 里条件表达式只属于 `sign` 那一项（元组右边是 `0` 和 `(1 if ... else -1)`）；空格不属于任何分支，被自然跳过；`-` 作一元负号时 `num` 为 `0`，`sign * 0` 无害，所以不用单独判断一元还是二元。

---
id: tlc-basic-calculator-iii-2-code
node: b.basic-calculator-iii
type: qa
step: 2
---
## Q
**LC 772 基本计算器 III**｜写出 Python 实现

字符串 `s` 是只含非负整数、`+ - * /` 和括号的有效表达式（长度 `1..10^4`，中间结果在 32 位整数内，除法截去小数部分，不能用 `eval`）。返回它的值。要求一遍扫描，括号可以嵌套很深。

## A
**思路。** 扫描字符串，数字累积到 `num`。遇到运算符或括号时，先用「待用运算符 `op`」把 `num` 并入当前层的项列表：`+` 追加、`-` 追加负数、`*` `/` 改写最后一项。遇到 `(` 就把当前层和 `op` 压栈并新开一层；遇到 `)` 就把这一层求和，弹出外层，求出的值作为外层的 `num`。末尾补一个 `+` 来冲刷最后一个数，答案是最外层所有项之和。

```python
def trunc_div(a: int, b: int) -> int:
    q = abs(a) // abs(b)               # 先按绝对值整除，再补符号：向零截断
    return q if (a < 0) == (b < 0) else -q


def calculate(s: str) -> int:
    saved: list[tuple[list[int], str]] = []   # 进入括号前的 (外层各项, 括号前的运算符)
    terms: list[int] = []              # 当前层的加法项：加减号只负责决定项的符号
    op, num = "+", 0                   # num 前面等待结合的运算符；正在读的数

    def apply() -> None:               # 把 num 按 op 并入当前层
        if op == "+":
            terms.append(num)
        elif op == "-":
            terms.append(-num)
        elif op == "*":
            terms[-1] *= num           # 乘除立刻与上一项结合
        else:
            terms[-1] = trunc_div(terms[-1], num)

    for ch in s + "+":                 # 末尾补一个 "+"，把最后一个数冲刷进去
        if "0" <= ch <= "9":
            num = num * 10 + int(ch)
        elif ch == "(":
            saved.append((terms, op))  # 暂存外层，开一层新的
            terms, op, num = [], "+", 0
        else:                          # + - * / )
            apply()
            if ch == ")":
                value = sum(terms)     # 括号内算完，它就是外层的一个“数”
                terms, op = saved.pop()
                num = value
            else:
                op, num = ch, 0
    return sum(terms)
```

运行：`s="1+1"` → `2`，`s="6-4/2"` → `4`，`s="2*(5+5*2)/3+(6/2+8)"` → `21`，`s="(0-3)/2"（负数商向零截断）` → `-1`，`s="((2+3))*4"` → `20`，`s="7"` → `7`，`嵌套 4999 层括号 + 数字 1` → `1`。

**复杂度。** 时间 `O(n)`：每个字符处理常数次，每项最多被并入一次、`sum` 每层只算一次；空间 `O(n)`：括号嵌套深度和各层的项列表，最坏 `n/2` 层。

**写法要点。** `for ch in s + "+"` 用哨兵避免循环外重复写一遍冲刷逻辑；嵌套函数 `apply` 读取外层的 `op`、`num`、`terms`（它们在每次调用前已被赋好，`apply` 只读取并修改 `terms` 的内容，所以不需要 `nonlocal`）；`terms, op = saved.pop()` 元组解包一步恢复外层现场；`"0" <= ch <= "9"` 比 `ch.isdigit()` 更严格（`isdigit` 对上标数字等也返回真）；`sum(terms)` 在每层结束时一次求和；`trunc_div` 用绝对值整除再补符号，避开 `int(a / b)` 的浮点路径。

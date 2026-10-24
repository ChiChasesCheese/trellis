---
id: tlc-basic-calculator-iii-5-alt
node: b.basic-calculator-iii
type: qa
step: 5
---
## Q
**LC 772 基本计算器 III**｜另一种解法

除了显式栈，还有别的写法吗？为什么面试里常见递归下降，它的风险是什么？

## A
**递归写法。** 遇到 `(` 就递归解析括号内部，直到匹配的 `)`，把返回的值当作一个数。代码和显式栈版逻辑完全对应，只是「栈」换成了调用栈：

```python
def trunc_div(a: int, b: int) -> int:
    q = abs(a) // abs(b)               # 向零截断
    return q if (a < 0) == (b < 0) else -q


def calculate_recursive(s: str) -> int:
    s += "+"                                   # 哨兵：冲刷最后一个数
    def parse(i: int) -> tuple[int, int]:      # 从 i 解析到匹配的 ")" 或末尾，返回 (值, 下一个位置)
        terms: list[int] = []
        op, num = "+", 0
        while i < len(s):
            ch = s[i]
            if "0" <= ch <= "9":
                num = num * 10 + int(ch)
            elif ch == "(":
                num, i = parse(i + 1)          # 递归求括号内的值，当作一个数
                continue
            else:
                if op == "+":
                    terms.append(num)
                elif op == "-":
                    terms.append(-num)
                elif op == "*":
                    terms[-1] *= num
                else:
                    terms[-1] = trunc_div(terms[-1], num)
                if ch == ")":
                    return sum(terms), i + 1
                op, num = ch, 0
            i += 1
        return sum(terms), i

    return parse(0)[0]
```

`parse(i)` 返回 `(这一层的值, 下一个要读的位置)`；`)` 时返回给上一层，上一层用返回的位置继续往后读。

**风险。** 括号嵌套深度等于递归深度，Python 默认上限约 `1000`。`"(" * 4999 + "1" + ")" * 4999` 这种合法输入（长度不到 `10^4`）会触发 `RecursionError`。可以 `sys.setrecursionlimit(20000)`，但深递归还可能耗尽 C 栈，不稳妥。

**怎么选。** 嵌套浅、语法复杂（有幂、函数调用、一元运算）时，递归下降更好扩展，容易对照文法写；此处长度到 `10^4`、嵌套可以很深，显式栈更稳。面试里先写显式栈，被追问再给出递归并指出两者的对应关系。另一种经典做法是**调度场算法**（两个栈：数栈和运算符栈，按优先级弹栈），适合运算符种类多的场合，但代码比项列表法长。

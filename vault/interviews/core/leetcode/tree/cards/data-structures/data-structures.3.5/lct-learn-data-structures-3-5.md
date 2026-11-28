---
id: lct-learn-data-structures-3-5
node: data-structures.3.5
type: qa
step: 1
---
## Q
**常用数据结构 › 栈 › 表达式解析**｜学习卡

套路是什么？

## A
**一句话。** 一遍扫描，数字一位位累积，读到运算符（或末尾）才结算前一个运算符 `op` 对应的数：加减压栈，乘除当场与栈顶合并，最后求和；括号和嵌套就是把被打断的外层上下文压栈或递归，内层算完当作一个数交还。

下图：一遍扫描的控制流；`op` 永远是当前数字之前的那个运算符。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 285">
<rect x="53.9" y="7.5" width="232.2" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读字符 c；数字就 num = num·10 + c</text>
<polygon points="95.0,72.0 104.0,59.5 236.0,59.5 245.0,72.0 236.0,84.5 104.0,84.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c 是运算符或已到末尾？</text>
<polygon points="98.2,124.0 107.2,111.5 232.8,111.5 241.8,124.0 232.8,136.5 107.2,136.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="128.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按前一个 op 结算 num</text>
<rect x="32.7" y="160.0" width="104.6" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+ ：push num</text>
<text x="85" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">- ：push -num</text>
<rect x="195.2" y="160.0" width="119.7" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="255" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">* / ：栈顶与 num</text>
<text x="255" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">当场合并</text>
<rect x="110.8" y="225.5" width="118.5" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="242.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">op = c，num = 0</text>
<path d="M 170.0 32.5 L 170.0 59.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,59.5 167.0,53.2 173.0,53.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 95.0 72.0 L 20.0 72.0 L 20.0 20.0 L 53.9 20.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="53.9,20.0 47.6,23.0 47.6,17.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="12" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 170.0 84.5 L 170.0 111.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,111.5 167.0,105.2 173.0,105.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178.0" y="102.0" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 170.0 136.5 L 170.0 145.0 L 85.0 145.0 L 85.0 160.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,160.0 82.0,153.7 88.0,153.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 136.5 L 170.0 145.0 L 255.0 145.0 L 255.0 160.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,160.0 252.0,153.7 258.0,153.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 85.0 200.0 L 85.0 238.0 L 110.8 238.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="110.8,238.0 104.4,241.0 104.4,235.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 255.0 200.0 L 255.0 238.0 L 229.2 238.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="229.2,238.0 235.6,235.0 235.6,241.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="278" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扫完：答案 = sum(st)</text>
</svg>

```python
def calculate(s):                    # LC 227（无括号）
    st, num, op = [], 0, '+'         # st：已定型的加法项
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if c in '+-*/' or i == len(s) - 1:   # 读完一个数
            if op == '+':
                st.append(num)
            elif op == '-':
                st.append(-num)
            elif op == '*':
                st.append(st.pop() * num)
            else:
                st.append(int(st.pop() / num))   # 向零取整
            op, num = c, 0           # op 永远是 num 之前的符号
    return sum(st)
```

**要点。**
- 为什么对？：表达式是若干项之和，项由 `*` `/` 连接；乘除优先级高，读完一个数就与栈顶合并，加减只压带符号的项。`op` 记的是 `num` 之前的运算符，所以要等下一个运算符或末尾才结算。
- LC 224、LC 772 怎么改？：遇 `(` 递归调用同一个解析函数，返回的和当作 `num`，遇 `)` 结算后返回；开头的负号等价于先结算 `0`。
- LC 394、LC 726 怎么改？：394 栈存 `(前缀, 倍数)`，`]` 时 `cur = prefix + cur * times`；726 栈存计数器，`(` 压新计数器，`)` 后读倍数乘进外层。
- LC 150、LC 8 怎么改？：150 无括号无优先级，遇运算符弹两个数（先弹出的是右操作数）；8 不用栈，是空格、符号、数字三阶段状态机，边读边截断到 `int32`。

**易错点。**
- 末尾没有结算最后一个数：`"3+2"` 应得 `5`，漏了得 `3`。
- 除法用 `//`：`"14-3/2"` 应得 `13`，`-3 // 2 = -2` 会得 `12`，要 `int(-3 / 2) = -1`。
- LC 150 操作数顺序反了：`["4","13","5","/","+"]` 应得 `6`。

**对应题目。** LC 150 逆波兰表达式求值、LC 394 字符串解码、LC 8 字符串转换整数 (atoi)、LC 224 基本计算器、LC 227 基本计算器 II、LC 726 原子的数量、LC 772 基本计算器 III

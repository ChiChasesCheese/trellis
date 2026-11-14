---
slug: parse-lisp-expression
---
## Q
**LC 736 Lisp 语法解析**｜Hard

求表达式的值：整数、变量、`(add a b)`、`(mult a b)`、`(let v1 e1 v2 e2 … expr)`；`let` 依次赋值，变量按从内到外的作用域查找。

## A
**一句话。** 切成 token 后递归下降：每次读一个完整表达式；`let` 复制一份环境做内层作用域，交替读「变量名、值」，遇到 `(` 或后面紧跟 `)` 的 token 就是返回式。

```python
def evaluate(expression):
    tokens = expression.replace('(', ' ( ').replace(
        ')', ' ) ').split()
    pos = 0

    def parse(env):          # 读一个完整表达式，返回它的值
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if tok != '(':
            if tok[0] == '-' or tok[0].isdigit():
                return int(tok)
            return env[tok]
        op = tokens[pos]
        pos += 1
        if op == 'let':
            env = dict(env)              # 内层作用域
            while True:
                tok = tokens[pos]
                if tok == '(' or tokens[pos + 1] == ')':
                    val = parse(env)     # 最后一个是返回式
                    break
                pos += 1                 # 变量名
                env[tok] = parse(env)
        else:
            a, b = parse(env), parse(env)
            val = a + b if op == 'add' else a * b
        pos += 1                         # 跳过 ')'
        return val

    return parse({})
```

**复杂度。** 时间 `O(n^2)`（每层 `let` 复制环境），空间 `O(n^2)`。

**易错点。**
- `let` 直接改外层环境：退出 `let` 后外层变量被污染，要复制或用栈记录后恢复。
- 把 `let` 最后一个变量当成赋值：它后面紧跟 `)`，是返回式。

**追问。**
- 不复制环境？：每个变量一个值栈，进入 `let` 时压栈、退出时弹出，`O(n)`。
- 负数怎么识别？：首字符是 `-` 或数字的就是整数，变量名以小写字母开头。

**同模式。** LC 224 基本计算器、LC 394 字符串解码、LC 1106 解析布尔表达式、LC 726 原子的数量

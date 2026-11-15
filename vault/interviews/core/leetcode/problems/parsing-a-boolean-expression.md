---
slug: parsing-a-boolean-expression
---
## Q
**LC 1106 解析布尔表达式**｜Hard

布尔表达式只含 `t`、`f`、`!(e)`、`&(e1,e2,...)`、`|(e1,e2,...)`（可嵌套）。给合法的表达式字符串，返回它的值。

## A
**一句话。** 用栈从左到右扫：遇到 `)` 就弹出括号内的所有值，再弹出运算符，按运算符算出结果压回栈。

```python
def parse_bool_expr(expression):
    st = []
    for c in expression:
        if c == ",":
            continue
        if c != ")":
            st.append(c)             # t f ! & | ( 都入栈
            continue
        vals = set()
        while st[-1] != "(":
            vals.add(st.pop())       # 括号内的所有值
        st.pop()                     # 弹出 "("
        op = st.pop()
        if op == "!":
            st.append("f" if "t" in vals else "t")
        elif op == "&":
            st.append("f" if "f" in vals else "t")
        else:
            st.append("t" if "t" in vals else "f")
    return st[-1] == "t"
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `eval` 或手写优先级：没有中缀运算符，括号内是参数列表，栈最直接。
- 括号内用列表而不是集合时忘了判空：集合足以判断「有没有 `t`/`f`」，`&`、`|`、`!` 只关心这个。
- 忘了弹出运算符：`(` 前面的符号才是运算符，需要多弹一次。

**追问。**
- 递归下降怎么写？：读到运算符就递归解析括号里的每个子表达式，遇到 `,` 继续，遇到 `)` 结束。
- 为什么 `!` 也能用集合？：`!` 的括号里只有一个值，`"t" in vals` 就是它的值。

**同模式。** LC 772 基本计算器 III、LC 736 Lisp 语法解析、LC 224 基本计算器

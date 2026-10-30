---
id: uth-python-functions-decorators-1-first-class
node: python.functions-decorators
type: qa
step: 1
---
## Q
**def 做了什么，函数为什么能当数据传**｜Python · CPython 3.14

`ops = {"+": add, "-": sub}`，然后 `ops[t](a, b)`。函数怎么能像数字一样放进字典、当参数传？

## A
**背景。** 在 C 里，函数名是写死在代码里的固定地址。想「按符号选一种运算」，只能写一长串 if/else。Python 里 `def` 是一条运行时执行的语句。

**结构。** `def add(...)` 执行时，造出一个函数对象，再把名字 `add` 绑定到它。函数对象和别的对象一样：名字可以改指别处，也可以放进字典、列表，当参数传入，当返回值返回。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<text x="10" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ops 字典 键 → 函数对象</text>
<rect x="10" y="28" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">"+"</text>
<rect x="44" y="28" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="61" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="78" y1="40" x2="148" y2="40" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,40.0 142.0,43.0 142.0,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="150" y="28" width="70" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="185" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">add</text>
<rect x="10" y="60" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">"-"</text>
<rect x="44" y="60" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="61" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="78" y1="72" x2="148" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,72.0 142.0,75.0 142.0,69.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="150" y="60" width="70" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="185" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sub</text>
<rect x="10" y="92" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="27" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">"*"</text>
<rect x="44" y="92" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="61" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<line x1="78" y1="104" x2="148" y2="104" stroke-width="1.2" stroke="currentColor"/>
<polygon points="148.0,104.0 142.0,107.0 142.0,101.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="150" y="92" width="70" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="185" y="108" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">mul</text>
<rect x="10" y="134" width="320" height="114" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个函数对象里装着</text>
<rect x="20" y="164" width="148" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="94" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__code__</text>
<rect x="172" y="164" width="148" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="246" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__globals__</text>
<rect x="20" y="196" width="148" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="94" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__defaults__</text>
<rect x="172" y="196" width="148" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="246" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__closure__</text>
<text x="170" y="240" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代码 全局表 默认值 闭包</text>
</svg>
```

**细节。**

- 函数对象里装着代码对象 `__code__`、所在模块的全局表 `__globals__`、默认值元组 `__defaults__` 和闭包 `__closure__`。
- 一份代码可以对应许多函数对象：外层函数每调用一次，里面的 `def` 就执行一次，造出一个新的函数对象。
- `f(x)` 的括号，是对对象 `f` 发起调用。

**为什么。** 「做什么」也能当数据传：省掉长串分支，也是回调和装饰器的基础。

**例题：** LC 150 逆波兰表达式求值

给表示后缀表达式的字符串数组 `tokens`，运算符只有 `+ - * /`，整数相除向零截断，求表达式的值。`1 <= tokens.length <= 10^4`。

```python
def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),
    }
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    return stack[0]
```

---
id: py-out-evaluation-short-circuit
node: output.evaluation
type: qa
step: 2
---
## Q
**and、or 与海象运算符**｜读代码说输出

```python
def f(tag):
    print("call", tag)
    return tag
print(0 or [] or "x")
print(1 and 2 and 0)
print(f(0) and f(1))
print(f(0) or f(2))
if (a := f(0)) and (b := f(1)):
    pass
print(a, "b" in globals())
```

输出什么？

## A
**输出。**

```
x
0
call 0
0
call 0
call 2
2
call 0
0 False
```

**为什么。**

- `or` 返回第一个真值操作数，都为假则返回最后一个；`and` 返回第一个假值操作数，都为真则返回最后一个。返回的是操作数本身，不是 True / False。
- 一旦结果确定就不再求值右边：`f(0) and f(1)` 只调用 `f(0)`。
- 海象运算符（walrus，`:=`）在表达式里赋值：`a` 被赋成 0，但 `and` 已短路，`b := f(1)` 没执行，所以 `b` 不存在。

**语言为什么这样设计。**

- 返回操作数而不是布尔值，让 `name or "default"` 这种写法成立；在 Python 2.5 加入条件表达式之前，这是常见的三元运算符替代写法。
- JavaScript 的 `||` 同样返回操作数；C 和 Java 的 `||` 只返回布尔值，不能这样用。

**怎么写才对。**

```python
x = v if v is not None else d    # 0、"" 是合法值时别用 or
```

**面试里一句话。**

The and and or operators short-circuit and return one of their operands, not a boolean, so an assignment hidden on the right side may never run.

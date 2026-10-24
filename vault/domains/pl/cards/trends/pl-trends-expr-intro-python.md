---
id: pl-trends-expr-intro-python
node: trends.expression-orientation
type: qa
step: 4
---
## Q
Python 里的条件表达式、`lambda`、推导式和海象运算符（`:=`）各是什么？它们怎样给一门语句导向的语言补上表达式能力，又有什么边界？

## A
Python 的 `if`、`for`、`while`、`try` 是语句，赋值 `x = 1` 也是语句，不能放进表达式。语言通过几个专门的表达式形式补足：

- **条件表达式**：`a if cond else b`，条件在中间。`label = "big" if n > 3 else "small"`。
- **推导式**：`[f(x) for x in xs if p(x)]`，把循环加过滤写成一个值，同样有 `{...}` 集合与字典版本。
- **`lambda`**：匿名函数，但**只能包含一个表达式**，不能放语句。
- **海象运算符** `:=`（Python 3.8）：在表达式里赋值并返回该值。

```python
nums = [m.group() for s in ["a1", "b", "c3"] if (m := re.search(r"\d", s))]
# ['1', '3']
```

海象在这里同时完成“匹配”和“判断是否成功”，避免调用两次 `re.search`。

**边界**（真实报错）：把语句放进需要表达式的位置会得到语法错误，例如 `eval("x = 1")` 得到 `SyntaxError: invalid syntax`。`try`/`except` 没有表达式形式，所以“失败时给默认值”只能写语句。

**优先级陷阱**：条件表达式的优先级很低。`print("x=" + "a" if x else "b")` 实际解析成 `("x=" + "a") if x else "b"`，当 `x` 为假时真实输出是 `b`，而不是 `x=b`。

**要记住的一点**：Python 的哲学是“简单优于复杂，可读性很重要”。它只补上最常用的表达式形式，并故意让 `lambda` 保持很小，把复杂逻辑推向命名函数。

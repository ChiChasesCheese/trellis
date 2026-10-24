---
id: tlc-python-idioms-4-walrus
node: python.idioms
type: qa
step: 4
---
## Q
**Python 工具箱｜海象运算符 `:=`**

什么时候用 `:=` 能把「先算、再判断、再使用」压成一步？哪些场合不该用？

## A
`name := expr` 在表达式里赋值并返回该值（3.8+）。适合**一个值既要判断又要复用**的地方。

```python
data = [1, 2, 3, 4, 5, 6]
if (n := len(data)) > 5:          # 先算长度再判断，n 之后还要用
    print("long", n)
while chunk := data[:2]:          # 切到空列表时是假值，循环自然结束
    data = data[2:]
    print(chunk)                  # [1, 2] / [3, 4] / [5, 6]
```

- 经典用法：`while (node := stack.pop()) ...`、正则 `if (m := re.match(p, s)):`、推导式里避免重复计算：

```python
res = [y for x in range(6) if (y := x * x) > 5]   # [9, 16, 25]：y 算一次，既过滤又收集
```

- 在记忆化里「查缓存 → 没有再算」：`if (v := memo.get(k)) is not None: return v`，一行完成。
- LC 3 里 `if last.get(ch, -1) >= left` 这类判断不需要它；**可读性优先**：只有省掉一个临时变量能让逻辑更紧凑时才用。
- **坑**：`:=` 在推导式里赋的变量会泄露到外层作用域（和普通循环变量不同）；顶层语句 `x := 1` 是语法错误，必须加括号 `(x := 1)`。

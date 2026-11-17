---
id: debugging-prevent-sibling-hunt
node: debugging.prevent
type: qa
step: 2
---
## Q
你刚修好一个缺陷：用 `abs(a - b)` 算“距离开演还有几天”，把已经过去的演出也算进了“即将开演”。提交之前，还应该做哪一步？怎么做？

## A
**把缺陷抽象成一个“模式”，在全仓库里搜同类**

- **缺陷很少孤立**：同一个人、同一天、同一个误解，会写出不止一处；
- **先抽象再搜**：不要只搜这行代码，搜它的形状。这里的形状是“对时间差取绝对值”，会丢掉方向；
- **文本搜索够用就用**：`rg "abs\("`；需要看结构时，用 `ast` 按语法树找，不被换行和变量名打乱；
- **每个命中都要看一遍**：有的是真的需要绝对值（求误差），有的是同一个缺陷，不能批量替换；
- **找到的同类缺陷各配一条测试**，并在提交说明里写清楚“同类问题还查了哪里”。

```python
import ast

src = """
gap = abs(show - today)
err = abs(measured - target)
n = abs(delta)
"""
for node in ast.walk(ast.parse(src)):
    if (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "abs"
            and isinstance(node.args[0], ast.BinOp) and isinstance(node.args[0].op, ast.Sub)):
        print("第", node.lineno - 1, "行：abs(差值)，方向丢了？")   # 命中第 1、2 行
```

命中里 `measured - target` 是在算误差，绝对值是对的；`show - today` 才是缺陷的同类。

**知识点：**防止复发（Prevent Recurrence）

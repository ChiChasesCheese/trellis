---
id: ai-failure-modes-scope-creep
node: ai.failure-modes
type: qa
step: 4
---
## Q
你让智能体修一个函数，它顺手加了缓存、改了另一个函数的签名、还新建了基类。为什么要拦，怎么低成本地发现？

## A
**diff 之外的改动没有人为它写过测试**

- **为什么拦**：公开的函数名、参数和返回值是外部依赖的合同，改了就是破坏；缓存和新抽象带来新的状态与失效问题，而合同没要求；
- **指令里先说清**：“只改这个函数；不动测试；不动公开签名”；
- **回来后核对**：列出被改动的函数、被改签名的函数和新增的名字，范围外的一律还原；
- **机械做法**：用 `ast` 比较前后的源码，不用肉眼从长 diff 里找。

```python
import ast

def snapshot(src: str):
    fns = [n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)]
    return {n.name: (ast.unparse(n.args), ast.dump(n)) for n in fns}

before = snapshot("def total(xs): return sum(xs)\ndef fmt(x): return str(x)\n")
after = snapshot("def total(xs, cache={}): return sum(xs)\ndef fmt(x): return f'{x}'\ndef _memo(): ...\n")
print("signature changed:", [n for n in before if before[n][0] != after[n][0]])
print("body changed:", [n for n in before if before[n][1] != after[n][1]])
print("new:", sorted(set(after) - set(before)))
```

<details class="pt"><summary>延伸</summary>

这段只比较顶层函数。类的方法、模块级常量同理，递归遍历即可。最简单的兜底仍然是让版本管理工具列出被改动的文件，范围外的文件出现就是警报。

</details>

**知识点：**AI 的典型错误（Failure Modes）

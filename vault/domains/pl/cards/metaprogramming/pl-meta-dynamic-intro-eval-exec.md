---
id: pl-meta-dynamic-intro-eval-exec
node: metaprogramming.dynamic-features
type: qa
step: 5
---
## Q
Python 的 `eval` 和 `exec` 是什么？它们和普通的函数调用有什么本质不同，一个例子里它们怎样工作？

## A
**是什么**：解释器本身就在运行时可用，所以 Python 把它开放成两个内置函数：
- `eval(字符串)`：把字符串当作**一个表达式**编译并求值，返回结果。
- `exec(字符串, 命名空间)`：把字符串当作**一段语句**编译并执行，可以定义函数、类，副作用写进给定的命名空间。

**心智模型**：把文本变成代码。程序运行中拼出一段源码，交给解释器，就像你自己写了这段代码一样。

```python
eval("1+2")                                    # 3
ns = {}
exec("def f(x): return x*2", ns); ns["f"](4)   # 8
eval("__import__('os').path.basename('/etc/passwd')")   # 'passwd'
```

真实输出依次是 `3`、`8`、`passwd`。第三行说明了问题：字符串里的内容可以调用任何东西，包括导入 `os`。如果这个字符串来自用户输入，就等于让用户在你的进程里执行任意代码。

**合理用途**：`dataclass` 用 `exec` 生成 `__init__`；`namedtuple` 老版本也这样做；REPL、Jupyter、模板引擎、表达式计算器。这些场景里字符串由库作者控制，不是外部输入。

**要记住的一点**：`eval` 不是沙箱。想要把外部输入的字面量解析成 Python 值，用 `ast.literal_eval`，它只接受字面量，不会执行函数调用。

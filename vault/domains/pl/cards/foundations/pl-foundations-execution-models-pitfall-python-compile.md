---
id: pl-foundations-execution-models-pitfall-python-compile
node: foundations.execution-models
type: qa
step: 6
---
## Q
Python 会先把源码编译成字节码再执行，为什么函数里引用了不存在的变量，加载文件时却不报错？

## A
Python 的「编译」只做语法分析并生成字节码，不做名字解析和类型检查。变量名是在函数真正执行到那一行时，才去全局和内建命名空间里查找。

```python
def f():
    return nope        # 加载文件时不会报错

print("loaded")
f()
```

实际输出：先打印 `loaded`，然后在调用 `f()` 时抛出 `NameError: name 'nope' is not defined`。如果这个分支只在罕见条件下才执行，错误可能几个月后才在线上暴露。

对照：同样的拼写错误，Go 在 `go build` 时就报 `undefined`，Rust 和 Java 也在编译期拒绝。所以「编译成字节码」不等于「编译期检查」：执行模型（字节码加解释器）和类型检查时机（静态或动态）是两条独立的轴。补救办法是用 `pyflakes`、`ruff` 或 `mypy` 这类静态工具，在运行之前把这类错误找出来。

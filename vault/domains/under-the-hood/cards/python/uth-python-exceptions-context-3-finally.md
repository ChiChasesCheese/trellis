---
id: uth-python-exceptions-context-3-finally
node: python.exceptions-context
type: qa
step: 3
---
## Q
**finally 保证到什么程度**｜Python · CPython 3.14

`try` 里 `return` 了、抛异常了，`finally` 还会执行吗？`finally` 里自己 `return` 又会怎样？

## A
**背景。** 打开的文件、拿到的锁，不管怎么离开都要归还。要是在每个出口手写清理，总会漏掉某条路：提前 `return`、中途抛错、`break`。

**结构。** `finally` 是语言保证的「出口清理」：`try` 里正常走完、用 `return` / `break` / `continue` 离开、抛异常离开，都会先执行 `finally`。异常离开时，异常先被暂存，`finally` 跑完再重新抛出。

**细节。**

- `finally` 里又抛新异常：旧异常挂到新异常的 `__context__` 上，回溯里两段都能看到。
- `finally` 里写 `return` / `break` / `continue`：暂存的异常被直接丢弃。3.14 起编译器会给 `SyntaxWarning`（PEP 765）。

```python
def f():
    try:
        1 / 0
    finally:
        return 42   # f() 返回 42，ZeroDivisionError 消失
```

**坑。** 这些情形不会执行 `finally`：`os._exit()`（直接退出、不跑清理）、进程被 `kill -9`（信号 `SIGKILL` 无法捕获）、断电。`Ctrl+C` 引发的 `KeyboardInterrupt` 是普通异常，`finally` 照常执行。

**对应 LeetCode：** 无直接对应的题

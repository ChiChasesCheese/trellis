---
id: py-out-exceptions-try-else-order
node: output.exceptions
type: qa
step: 2
---
## Q
**try、except、else、finally 的顺序**｜读代码说输出

```python
def f(x):
    try:
        print("try")
        if x: raise ValueError
    except ValueError:
        print("except")
        return "r1"
    else:
        print("else")
        return "r2"
    finally:
        print("finally")
print(f(False))
print(f(True))
```

输出什么？

## A
**输出。**
```
try
else
finally
r2
try
except
finally
r1
```

**为什么。**
- 没有异常：try 跑完 → 执行 `else` → 最后 `finally`，然后才把 `else` 里的返回值 "r2" 交给调用者。
- 抛出 ValueError：跳过 `else`，进入匹配的 `except`，`return "r1"` 时先去执行 `finally`，再返回。
- 所以 `print("finally")` 总是出现在外层 `print` 打印返回值之前。

**语言为什么这样设计。**
- `else` 只在 try 成功时运行，把“可能抛异常的那一行”和“成功之后的逻辑”分开，这样 `except` 不会误捕获后面代码里的同类异常。
- `finally` 不论正常、异常、return 都执行，等价于其他语言的 `finally`；Java 没有 try 的 `else`，C++ 靠析构函数（RAII）清理，Python 里更常用 `with`。

**怎么写才对。**
```python
try:
    data = load()          # 只放会抛异常的那一句
except OSError:
    data = None
else:
    process(data)          # 成功后的逻辑，抛的错不会被上面的 except 吞
```

**面试里一句话。**
`else` runs only when the try body raised nothing, and `finally` always runs before the function actually returns.

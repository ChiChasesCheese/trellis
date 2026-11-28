---
id: py-out-exceptions-finally-return
node: output.exceptions
type: qa
step: 1
---
## Q
**finally 里的 return**｜读代码说输出

```python
def f():
    try:
        return "try"
    finally:
        return "finally"
print(f())
```

输出什么？（Python 3.14）

## A
**输出。**
```
finally
```
3.14 起，运行（编译）这个文件还会在 stderr 打印 `SyntaxWarning: 'return' in a 'finally' block`。

**为什么。**
- `return "try"` 先算出返回值，但在真正返回前必须执行 `finally` 块。
- `finally` 里的 `return` 直接结束函数，覆盖掉先前的返回值。
- 同样的道理，`finally` 里 return（或 break、continue）还会吞掉正在传播的异常，错误悄悄消失。

**语言为什么这样设计。**
- `finally` 保证清理一定执行；在它里面跳出控制流的语义是有定义的，只是几乎总是 bug。PEP 765（3.14）因此加了编译期警告，是否升级为错误留给以后。
- Java 同样允许 `finally` 里 return 并吞异常（`javac -Xlint:finally` 会警告）；JavaScript 也一样，而 C# 直接禁止从 `finally` 跳出。

**怎么写才对。**
```python
try:
    return compute()
finally:
    cleanup()        # 只做清理，不 return、不 break
```

**面试里一句话。**
A `return` inside `finally` overrides the pending return value and swallows any in-flight exception, which Python 3.14 now warns about.

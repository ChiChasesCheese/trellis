---
id: errors-cleanup-finally-masks
node: errors.cleanup
type: qa
step: 2
---
## Q
`finally` 块里再出一个异常、或者写了 `return`，原来的异常会怎样？清理代码应该守什么规矩？

## A
**清理代码不能再出事，更不能 return**

- **`finally` 里的 `return` 吞掉异常**：函数正常返回，原来的错误无声消失；
- **`finally` 里抛新异常会顶替原异常**：调用方看到的是 `close()` 的失败，真正的原因只挂在 `__context__` 上；
- **所以清理要小而稳**：只做释放，不做校验、不做业务判断；
- **释放本身可能失败时**：捕获它并记日志，不让它顶掉主线的异常；
- **多个资源各自释放**：一个失败不能让后面的资源不释放。

```python
def swallowed():
    try:
        raise ValueError("原始错误")
    finally:
        return "ok"                  # 吞掉了 ValueError

print(swallowed())                   # ok：没人知道出过错

try:
    try: raise ValueError("原始错误")
    finally: raise OSError("close 失败")      # 顶替原异常
except OSError as e: print(repr(e.__context__))   # ValueError('原始错误')
```

<details class="pt"><summary>延伸</summary>

Python 3.14 起，`finally` 里的 `return`、`break`、`continue` 会让编译器发 `SyntaxWarning`（PEP 765），正是因为它们吞异常。

</details>

**知识点：**所有路径上的清理（Cleanup on Every Path）

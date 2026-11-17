---
id: errors-values-two-styles
node: errors.exceptions-vs-values
type: qa
step: 1
---
## Q
失败既可以抛异常，也可以返回一个值（`None`、`False`、错误码、结果对象）。怎么选？两种风格各自的代价是什么？

## A
**常见、要马上分支的返回值；罕见、要穿过多层的抛异常**

- **异常不会被忘**：调用方不处理，它就一路冒上去，直到有人接或者进程停下；
- **返回值可以被忽略**：忘了检查，程序带着错误结果继续往下跑；
- **异常是不可见的跳转**：函数签名里看不出会抛什么，中间每一层都可能被打断，清理要靠 `finally`；
- **返回值要一层层传**：每层都要写 `if`，深层的失败要手工往上带；
- **Python 的成本**：不抛时，`try` 块几乎免费（3.11 起零开销实现）；真抛出才贵，所以别拿异常做每次循环都会发生的普通分支。

```python
accounts = {"a": 100}

def find(account_id: str) -> int | None:
    return accounts.get(account_id)        # 查不到是日常：返回 None，调用方立刻分支

def withdraw(balance: int, n: int) -> int:
    if n > balance:
        raise ValueError("insufficient")   # 违反调用前提：别让它被忽略
    return balance - n

print(find("zz"), withdraw(100, 30))       # None 70
```

**知识点：**异常与错误值（Exceptions vs Values）

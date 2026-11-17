---
id: errors-chaining-exception-group
node: errors.chaining
type: qa
step: 3
---
## Q
一批并发任务有好几个都失败了，只抛第一个异常会丢掉什么？怎么把多个失败一起交给调用方，调用方又怎么按类型分别处理？

## A
**多个失败装进 `ExceptionGroup`，用 `except*` 按类型拆开处理**

- **只抛第一个**：其余失败的原因没人知道，修好第一个，重跑又遇到第二个；
- **`ExceptionGroup("消息", [e1, e2, ...])`**（3.11 起）：一个异常里装多个，`eg.exceptions` 取出来；`asyncio.TaskGroup` 在子任务失败时也抛它；
- **`except* ValueError`**：只处理组里的 `ValueError`，剩下的自动重新抛出；多个 `except*` 可以并排，每个各取自己的那份；
- **`except*` 里不能 `return`、`break`、`continue`**，也不能和普通 `except` 混用；
- **取舍**：每个任务的失败彼此独立、调用方要逐个结果，就返回“一条一结果”；整件事失败、但多个原因都要报告时才用组。

```python
def run_all(tasks):
    errors = []
    for t in tasks:
        try: t()
        except Exception as e: errors.append(e)       # 收集，不在第一个就停
    if errors: raise ExceptionGroup("batch failed", errors)

def boom(exc):
    def f(): raise exc
    return f

try: run_all([boom(ValueError("a")), boom(TimeoutError("b")), boom(ValueError("c"))])
except* ValueError as eg: print("value", len(eg.exceptions))       # value 2
except* TimeoutError as eg: print("timeout", len(eg.exceptions))   # timeout 1
```

**知识点：**保留原因（Wrapping & Chaining）

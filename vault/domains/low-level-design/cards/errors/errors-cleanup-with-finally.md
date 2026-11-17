---
id: errors-cleanup-with-finally
node: errors.cleanup
type: qa
step: 1
---
## Q
为什么释放文件、锁、连接要用 `with` 或 `finally`，而不是在函数最后写一句 `close()`？

## A
**清理要挂在“离开”上，不挂在“走到末尾”上**

- **末尾的 `close()` 只在一条路径上执行**：中间任何一处 `raise`、`return`、`break` 都会绕过它，资源泄漏；
- **`finally` 在所有出口执行**：正常结束、抛异常、`return` 都会跑，之后异常继续往上传；
- **`with` 就是封装好的 `try/finally`**：进入时拿资源，退出时无论成败都释放，释放代码写在资源自己身上，调用方不会忘；
- **拿资源写在 `try` 之前**：拿失败说明什么都没拿到，没有东西可释放，不该进 `finally`；
- **自己的资源用 `@contextmanager`**：`yield` 前是获取，`finally` 里是释放。

```python
from contextlib import contextmanager

log = []

@contextmanager
def acquire(name):
    log.append(f"open {name}")
    try:
        yield name
    finally:
        log.append(f"close {name}")        # 正常、异常、return 都会走到这里

try:
    with acquire("f"): raise ValueError("boom")
except ValueError: print(log)              # ['open f', 'close f']
```

<details class="pt"><summary>延伸</summary>

`finally` 管不到的只有进程被直接杀死（`kill -9`、断电、`os._exit`）。那种情况靠下一次启动时的恢复：临时文件改名提交、事务日志、锁的租约过期。

</details>

**知识点：**所有路径上的清理（Cleanup on Every Path）

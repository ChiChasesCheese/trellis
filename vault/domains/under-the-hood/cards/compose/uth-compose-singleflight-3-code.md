---
id: uth-compose-singleflight-3-code
node: compose.singleflight
type: qa
step: 3
---
## Q
**不变量与核心代码**｜Go · golang.org/x/sync v0.24

哪些步骤必须在同一把锁里完成？用 Python 写出最小版本。

## A
**不变量。**

- `m[k]` 存在，当且仅当有一次 `fn` 正在执行
- 查 `m` 和登记在同一把锁里完成，否则两个线程会都以为自己先到
- `fn` 在锁外执行，否则一次慢调用会卡住整个 `Group`
- 先写 `val`、`err`，再唤醒等待者；等待者醒来后读结果，不必再加锁
- 唤醒和删记录放在同一段持锁代码里

```python
import threading
from types import SimpleNamespace
from typing import Any, Callable


class Group:
    def __init__(self) -> None:
        self.mu = threading.Lock()
        self.m: dict[str, SimpleNamespace] = {}   # key -> 正在进行的调用 (done 事件 + 结果)

    def do(self, key: str, fn: Callable[[], Any]) -> Any:
        with self.mu:                             # 判断先后和登记：同一把锁里一次完成
            call = self.m.get(key)
            leader = call is None
            if leader:
                call = self.m[key] = SimpleNamespace(done=threading.Event(), val=None, err=None)
        if leader:
            try:
                call.val = fn()                   # 先到者在锁外真正执行
            except BaseException as e:
                call.err = e
            finally:
                with self.mu:
                    call.done.set()               # 先唤醒等待者
                    del self.m[key]               # 再摘记录，下次重新执行
        else:
            call.done.wait()                      # 后到者只等结果，不执行 fn
        if call.err:
            raise call.err
        return call.val
```

例：三个线程同时 `do("k", slow)`，`slow` 只执行一次，三个线程拿到同一个返回值。

**对应 LeetCode：** 无直接对应的题

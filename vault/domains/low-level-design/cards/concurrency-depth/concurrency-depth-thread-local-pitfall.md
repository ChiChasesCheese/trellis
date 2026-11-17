---
id: concurrency-depth-thread-local-pitfall
node: concurrency-depth.confinement
type: qa
step: 4
---
## Q
用 `threading.local()` 存“当前用户”，在线程池和 `asyncio` 里各会出什么问题？

## A
**`threading.local` 跟线程走，不跟任务走**

- **线程池**：工作线程会被复用，上一个任务写进去的值留在那里。下一个任务如果没先赋值，读到的是别人的用户。示例里池里只有一个线程，第二个任务读到 `alice`；
- **做法**（示例展示的是没清理的写法）：任务入口先赋值，`finally` 里 `del`；或者干脆把用户当参数传下去；
- **`asyncio`**：所有协程在同一个线程里，`threading.local` 被所有任务共用。实测两个任务各自写入、`await` 之后再读，`alice` 的任务读到了 `bob`；
- **`contextvars.ContextVar`**：每个任务有自己的上下文副本，同样的实验两个任务各读到自己的值。它也适用于线程（`concurrent.futures` 不会自动拷贝上下文，要用 `contextvars.copy_context().run`）；
- **共享的前提是不变**：只读配置不需要 local，`local` 是给“每个线程各自一份可变状态”（比如数据库连接）用的。

```python
import threading
from concurrent.futures import ThreadPoolExecutor

tl = threading.local()
def handle(user):
    seen = getattr(tl, "user", None)      # 上一个任务留下的
    tl.user = user
    return seen

with ThreadPoolExecutor(max_workers=1) as ex:
    print(list(ex.map(handle, ["alice", "bob", "carol"])))
# [None, 'alice', 'bob']：池复用线程，值串了任务
```

**知识点：**不靠锁的线程安全（Immutability & Confinement）

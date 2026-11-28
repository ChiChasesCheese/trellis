---
id: hi-c-sd-caching-b01-single-flight
node: sd.core-concepts.caching.beyond
type: qa
step: 1
---
## Q
**缓存 · 请求合并的实现**｜拓展 · 加分
请求合并（single flight）到底怎么实现？为什么锁不能把 load() 包起来？

## A
**模式。** 请求合并：同键的并发请求共享一次加载。

```python
import threading
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional


@dataclass
class _Call:
    done: threading.Event = field(default_factory=threading.Event)
    value: object = None
    error: Optional[BaseException] = None


class SingleFlight:
    def __init__(self) -> None:
        self._lock = threading.Lock()          # 只保护字典，不包住 load()
        self._inflight: Dict[str, _Call] = {}

    def do(self, key: str, load: Callable[[], object]) -> object:
        with self._lock:
            call = self._inflight.get(key)
            leader = call is None
            if leader:
                call = self._inflight[key] = _Call()
        if leader:
            try:
                call.value = load()
            except BaseException as e:         # 失败也要通知等待者，否则它们永远等
                call.error = e
            finally:
                with self._lock:
                    del self._inflight[key]    # 先摘掉，之后的新请求重新加载
                call.done.set()
        else:
            call.done.wait()
        if call.error:
            raise call.error
        return call.value
```
- **锁只保护"登记谁是领头者"：** 若把慢的 `load()` 包进锁里，所有键的请求都被串行化，等于没有并发。
- **每个键一个 `Event`：** 等待者阻塞在事件上而不是自旋；领头者 `set()` 后全体同时醒来。
- **失败要共享：** 领头者出错，等待者也拿到同一个异常，而不是各自再冲向数据库。
- **只在单进程内有效：** 多实例时每个实例各放一个请求，数据库最多收到"实例数"个请求；要跨实例，需用 Redis 里的短期分布式锁或租约，但这引入锁超时的问题。
- **命名：** Go 标准扩展库里的 `singleflight` 就是这个思路。

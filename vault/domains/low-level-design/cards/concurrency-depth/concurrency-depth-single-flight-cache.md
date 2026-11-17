---
id: concurrency-depth-single-flight-cache
node: concurrency-depth.safe-structures
type: qa
step: 2
---
## Q
`functools.lru_cache` 是线程安全的，为什么 8 个线程同时查同一个冷 key，加载函数还是被调用了很多次？线程安全的缓存要怎么写，才能让同一个 key 只加载一次？

## A
**线程安全只保证缓存结构不坏，不保证只加载一次**

- **`lru_cache` 的行为**：文档写明缓存是线程安全的，但函数可能被多次调用——别的线程在第一次调用完成并写入之前又来调用。实测 8 个线程同时查同一个 key（加载 5 ms），50/50 轮多次加载，3.11 和 3.14t 一样；
- **把加载整个放进锁里**：只加载一次，但所有 key 都排队，一个慢 key 挡住全部；
- **single-flight**：锁里只登记“这个 key 有人在加载”（放一个 `Future`），登记者在锁外加载并写结果，后来者等同一个 `Future`；
- **失败不缓存**：加载抛异常时把登记删掉，等待者拿到同一个异常，下一次请求重新加载；
- **锁里不做慢事**：登记和删除都很短，加载在锁外。

```python
import threading
from concurrent.futures import Future
class Cache:
    def __init__(self, load): self._load, self._lock, self._futs = load, threading.Lock(), {}
    def get(self, key):
        with self._lock:                       # 锁里只登记
            mine = key not in self._futs
            if mine: self._futs[key] = Future()
            fut = self._futs[key]
        if mine:                               # 登记者在锁外加载
            try: fut.set_result(self._load(key))
            except BaseException as e:
                with self._lock: del self._futs[key]   # 失败不缓存
                fut.set_exception(e)
        return fut.result()
```

<details class="pt"><summary>延伸</summary>

这个缓存没有容量上限也没有过期，真要上线还要加淘汰和 TTL；这两件事的状态同样要放在这把锁里改。

</details>

**知识点：**线程安全结构的写法（Thread-Safe Structures）

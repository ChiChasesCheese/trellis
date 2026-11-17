---
id: concurrency-depth-rate-limiter-lock
node: concurrency-depth.safe-structures
type: qa
step: 3
---
## Q
滑动窗口限流器的 `check()` 要清过期记录、比较数量、放行才追加、更新 `allowed` 和 `denied` 计数。哪些步骤要在同一把锁里？`stats()` 也要加锁吗？

## A
**判定、记账、计数同一把锁；读统计也拿它**

- **不变量**：窗口内的放行数不超过 `limit`，`allowed + denied` 等于调用总数。这两条分别由“比较和追加”“自增计数”维持，它们是复合操作；
- **实测（4 线程各调 50 次，limit=10，100 轮）**：不加锁在 3.11 上默认和 1e-6 都是 0/100（缺口里只有 C 方法调用，被 GIL 藏住），3.14t 默认间隔 21/100 轮放行数不对；加锁两个构建都是 0/100。3.11 上测不出，不代表这段代码在换成假时钟（Python 函数）或搬到 3.14t 后仍然对；
- **时钟在锁内读**：读时钟和判定是一个整体，否则两个线程拿到的时间顺序和判定顺序可能相反；
- **`stats()` 也拿同一把锁**：否则可能读到放行数已加、拒绝数还没加的中间状态；返回新字典，别暴露内部计数；
- **非法参数在锁外拒绝**，也不计入统计（示例省略了参数校验和 `stats()`，它们的写法就是上面说的）。

```python
import threading
from collections import deque
class Limiter:
    def __init__(self, limit, window, clock):
        self._limit, self._window, self._clock = limit, window, clock
        self._hits, self._lock, self._n = deque(), threading.Lock(), {True: 0, False: 0}
    def check(self) -> bool:
        with self._lock:
            now = self._clock()
            while self._hits and self._hits[0] <= now - self._window:
                self._hits.popleft()
            ok = len(self._hits) < self._limit
            if ok: self._hits.append(now)
            self._n[ok] += 1                   # 计数与判定同一把锁
            return ok
```

**知识点：**线程安全结构的写法（Thread-Safe Structures）

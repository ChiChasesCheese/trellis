---
id: concurrency-depth-one-lock-all-state
node: concurrency-depth.compound-actions
type: qa
step: 4
---
## Q
关注登记表和收件箱各有一把锁，每把锁内部都没问题；发布一条通知要先改登记表、再写收件箱。为什么读到的结果可能对应不了任何串行执行的顺序？

## A
**一个不变量跨几个结构，就用同一把锁罩住它们**

- **两把锁只保证各自的结构不坏**：登记表更新完、收件箱还没写的那一刻，另一个线程读到“登记了但没有通知”，这个状态在任何串行顺序里都不存在；
- **实测（3.11，2 个写线程各发 3000 条，1 个读线程同时检查两者相等，100 轮）**：两把锁 默认间隔 0/100，1e-6 下 100/100 轮读到不一致；一把锁两种间隔都是 0/100；3.14t 上两把锁 94/100；
- **默认间隔测不出**：写线程的缺口里恰好有调用才会被切开，别拿它当安全证明；
- **规则**：锁跟着不变量走，不跟着数据结构走；一次公开方法一次持锁，读也走同一把锁；
- **代价**：并发度降到一把锁。先正确，量出锁竞争之后再拆（按 key 分片，每片一把锁）。

```python
import threading
class Feed:
    def __init__(self):
        self._lock = threading.Lock()          # 罩住下面全部状态
        self._followers, self._inbox = {}, {}
    def follow(self, user, actor):
        with self._lock:
            self._followers.setdefault(actor, set()).add(user)
    def publish(self, actor, movie):
        with self._lock:                       # 算受众和写收件箱不可分
            for u in self._followers.get(actor, ()):
                self._inbox.setdefault(u, []).append(movie)
    def inbox(self, user):
        with self._lock:                       # 读也拿同一把锁
            return list(self._inbox.get(user, []))
```

**知识点：**复合操作（Compound Actions）

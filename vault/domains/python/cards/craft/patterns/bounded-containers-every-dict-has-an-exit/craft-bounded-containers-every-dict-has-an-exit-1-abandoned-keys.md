---
id: craft-bounded-containers-every-dict-has-an-exit-1-abandoned-keys
node: craft.patterns.bounded-containers-every-dict-has-an-exit
type: qa
step: 1
---
## Q
**有界容器 · 每个字典都要有出口：为什么「访问时顺手清理」清不掉不再回来的 key**｜模式

按用户限流的服务，内部是 `dict[用户, 滑动窗口]`。每来一个新用户就多一项，用户走了以后这一项没人删。常见的补救是「`allow` 里窗口过期了就顺手删掉这个用户」。这能让字典不再无限增长吗？

## A
**要点。** 不能。访问时的清理只能清**正在被访问**的 key，而需要被清的恰恰是**不会再来**的 key。一个只出现一次的用户，那次访问时它刚刚被记了一笔，窗口不空；之后它永远不会再来，清理代码永远没有机会执行。需要一个与具体 key 的访问无关的出口：`sweep`，由别人的访问摊还触发，或者定时触发。

```python
from collections import deque

class Limiter:
    """每个 key 一个滑动窗口：窗口内最多 limit 次。"""
    def __init__(self, limit, window, prune):
        self.limit, self.window, self.prune = limit, window, prune
        self.hits = {}

    def allow(self, key, now):
        q = self.hits.setdefault(key, deque())
        while q and now - q[0] >= self.window: q.popleft()
        ok = len(q) < self.limit
        if ok: q.append(now)
        if self.prune and not q: del self.hits[key]      # 只清自己，key 不回来就永远清不到
        return ok

    def sweep(self, now):                                # 与具体 key 无关的出口
        for k in [k for k, q in self.hits.items() if not q or now - q[-1] >= self.window]:
            del self.hits[k]

lim = Limiter(limit=1, window=10, prune=True)
for t in range(1000):
    lim.allow(f"user{t}", now=float(t))                  # 每个请求都是新用户，且不会再来
print("访问时顺手清理（prune）后，字典里还有", len(lim.hits), "个 key")
lim.sweep(now=2000.0)
print("显式 sweep 之后:", len(lim.hits))
```

1000 个只出现一次的用户：

```
访问时顺手清理（prune）后，字典里还有 1000 个 key
显式 sweep 之后: 0
```

**为什么。** 凡是 `dict[key, 状态]` 且 key 来自外部输入（用户、IP、会话、主题名），就必须问：这一项什么时候删？没有答案的字典在长期运行的服务里就是内存泄漏，而且在测试里永远看不到，因为测试只跑几秒。

**判据。** 回收一项的条件是「它与刚 new 出来的状态等价」（限流器里叫 `is_idle`）：此时留着和删掉对任何后续判定都没有区别，所以删除一定安全。

**代价。** `sweep` 要扫整个字典，O(条目数)；下一张卡讲怎样让它摊还成 O(1)。

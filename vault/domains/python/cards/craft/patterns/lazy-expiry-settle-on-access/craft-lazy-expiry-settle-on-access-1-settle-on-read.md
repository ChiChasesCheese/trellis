---
id: craft-lazy-expiry-settle-on-access-1-settle-on-read
node: craft.patterns.lazy-expiry-settle-on-access
type: qa
step: 1
---
## Q
**惰性过期 · 为什么不起后台线程清理，而是每次访问先结清**｜模式

缓存条目有 TTL。最直白的做法是起一个后台线程定期扫描删除过期条目。到了线程两次扫描之间，一个刚过期的条目被读到，会发生什么？不用线程怎么保证读到的永远正确？

## A
**要点。** 惰性过期（lazy expiry）：每次读写都先检查并清掉到期的东西，再做自己的事。读本身保证一致，不依赖「清理线程恰好跑过」。后台线程要处理启动关闭、与读写的竞态，测试还得 sleep；惰性结清这三样都省了。

```python
class SweeperStore:                       # 读不检查过期
    def get(self, k):
        item = self.data.get(k)
        return item[0] if item else None  # 清理线程没跑时，过期值被读出来

class LazyStore(SweeperStore):
    def get(self, k):
        item = self.data.get(k)
        if item is None:
            return None
        if item[1] <= Clock.t:            # 恰好到点也算过期（左闭右开）
            del self.data[k]              # 访问时顺手结清
            return None
        return item[0]
```

写入 ttl=10 的值，时钟走到 10：

```
SweeperStore t=10 读到: x
LazyStore t=10 读到: None
```

**为什么。** 过期与否只对「被问到」的那一刻有意义；没人问的时候，条目有没有被删，没有人在乎。

**代价。** 写入后再也没人访问的条目会一直占内存；到期事件（淘汰通知）发生在下一次访问时，不是准点。见第 3 张卡。

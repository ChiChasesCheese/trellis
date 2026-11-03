---
id: craft-lazy-expiry-settle-on-access-5-scales-redis
node: craft.patterns.lazy-expiry-settle-on-access
type: qa
step: 5
---
## Q
**惰性过期 · 从令牌管理器到 Redis 的惰性加主动删除**｜模式

LeetCode 的认证管理器、LLD 的 TTL 缓存、Redis 的过期键，用的都是惰性过期吗？到了大规模，纯惰性的内存问题怎么解决？

## A
**要点。** 是同一个思路。认证管理器每次 `renew` 或 `count_unexpired` 都先结清，过期的 token 不能续期，恰好到点算过期；Redis 访问键时检查并删除（惰性），再加周期性抽样删除一批过期键（主动），免得没人读的键永远占内存。DynamoDB 的 TTL 则交给后台异步清理，所以刚过期的条目可能还能被读到一会儿。

```python
def renew(self, token, now):
    self._settle(now)                      # 先结清：过期的 token 不能续期
    if token in self.exp:
        self.exp[token] = now + self.ttl

def _settle(self, now):
    self.exp = {t: e for t, e in self.exp.items() if e > now}   # 恰好到点算过期
```

ttl=5：a 在 1 生成，b 在 7 生成，a 在 6 续期（此刻已过期，被忽略），6 时刻计数：

```
1
```

**尺度对照。** 一个字典加时钟 → 加到期堆和显式 purge → 加周期抽样 → 后台异步清理并接受「读到短暂过期值」。越往后越不精确，越省读路径的成本。

**易错。** 如果产品要求「过期后绝不能读到」，就不能用异步清理，读路径上必须带过期检查。

**信号。** 过期数据多、读少；或需要准点通知。后者惰性做不到，必须有定时器。

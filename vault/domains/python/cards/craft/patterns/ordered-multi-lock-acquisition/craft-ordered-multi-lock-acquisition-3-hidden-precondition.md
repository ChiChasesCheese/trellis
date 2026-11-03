---
id: craft-ordered-multi-lock-acquisition-3-hidden-precondition
node: craft.patterns.ordered-multi-lock-acquisition
type: qa
step: 3
---
## Q
**固定顺序加多把锁 · 组合限流器为什么不许同一个限流器出现两次**｜模式

组合限流按规则列表顺序依次进入各规则的锁，规则顺序是固定的。组合限流器却在构造时拒绝同一个限流器被两条规则共用，理由写的是「锁序会依赖 key」。规则顺序固定，锁序不就固定了吗？

## A
**要点。** 不是。限流器内部是分片锁，拿哪把锁由 key 决定。同一个限流器出现在两条规则里时，请求 A 先后拿「分片 0、分片 1」，请求 B 的 key 不同，先后拿「分片 1、分片 0」，又是 ABBA。固定的顺序只在每条规则各用一个独立的限流器、其锁集合互不相交时才成立。这类前提必须由构造函数检查，而不是靠调用方记得。

```python
def lock_for(self, key):
    return self.shards[key % len(self.shards)].lock   # 锁由 key 决定

# A：规则1 用 key 0，规则2 用 key 1；B：规则1 用 key 1，规则2 用 key 0
# 若两条规则是同一个 Limiter：A 拿 shard0→shard1，B 拿 shard1→shard0

# 构造时守住前提
if len({id(rule.limiter) for rule in rules}) != len(rules):
    raise InvalidConfiguration("each rule needs its own RateLimiter ...")
```

两条规则共用一个限流器，与各用各的：

```
两条规则共用同一个限流器 -> 死锁: True
每条规则各用自己的限流器 -> 死锁: False
```

**为什么。** 「固定顺序」是对整个系统的全局承诺。只要有一个地方的顺序依赖数据，承诺就失效。

**易错。** 把前提写成注释而不是检查：下一个使用者不会读注释。

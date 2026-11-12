---
slug: design-authentication-manager
---
## Q
**LC 1797 设计一个验证系统**｜Medium

设计验证码系统：`generate` 生成、`renew` 续期未过期的验证码、`countUnexpiredTokens` 统计未过期数；验证码在 `t` 时刻过期，则 `t` 时刻起视为已过期。

## A
**一句话。** 哈希表只存每个验证码的过期时刻，`renew` 先判断「过期时刻 > 当前时刻」，`count` 数大于当前时刻的项。

```python
class AuthenticationManager:
    def __init__(self, timeToLive):
        self.ttl = timeToLive
        self.expire = {}      # tokenId -> 过期时刻，惰性判断

    def generate(self, tokenId, currentTime):
        self.expire[tokenId] = currentTime + self.ttl

    def renew(self, tokenId, currentTime):
        # 不存在取 0，已过期也不满足：都忽略
        if self.expire.get(tokenId, 0) > currentTime:
            self.expire[tokenId] = currentTime + self.ttl

    def countUnexpiredTokens(self, currentTime):
        return sum(t > currentTime
                   for t in self.expire.values())
```

**复杂度。** `generate`、`renew` 为 `O(1)`，`count` 为 `O(n)`，空间 `O(n)`。

**易错点。**
- 比较写成 `>=`：过期时刻恰为 `7` 时 `count(7)` 仍算 `1`，应为 `0`，过期优先。
- `renew` 不判存在或过期直接赋值：已过期的验证码被复活。

**追问。**
- `count` 想要 `O(1)`？：时间严格递增，用按过期时刻排序的有序字典或队列，惰性弹出队首过期项。

**同模式。** LC 146 LRU 缓存、LC 362 敲击计数器、LC 359 日志速率限制器、LC 981 基于时间的键值存储

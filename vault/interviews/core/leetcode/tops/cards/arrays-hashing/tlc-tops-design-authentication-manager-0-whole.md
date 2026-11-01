---
id: tlc-tops-design-authentication-manager-0-whole
node: arrays-hashing.design-authentication-manager
type: qa
---
## Q
**LC 1797 设计一个验证系统**｜Medium · 全公司热度第 109 名

设计带验证码的验证系统：每个验证码在 `currentTime` 之后 `timeToLive` 秒过期，被更新后从更新时刻起重新计时。实现 `AuthenticationManager(timeToLive)`：`generate(tokenId, currentTime)` 在该时刻生成新验证码；`renew(tokenId, currentTime)` 更新**未过期**的验证码，不存在或已过期则忽略；`countUnexpiredTokens(currentTime)` 返回该时刻未过期的验证码数。若验证码在时刻 `t` 过期，同一时刻 `t` 的 `renew` 或 `countUnexpiredTokens` 视为已过期。`1 <= timeToLive <= 10^8`，`1 <= currentTime <= 10^8`，`tokenId` 长度 `1` 到 `5`、只含小写字母，每次 `generate` 的 `tokenId` 都不同，所有调用的 `currentTime` 严格递增，总调用不超过 `2000` 次。例：`timeToLive = 5`，`renew("aaa", 1)` 忽略，`generate("aaa", 2)`，`countUnexpiredTokens(6)` → `1`，`generate("bbb", 7)`，`renew("aaa", 8)` 忽略（`aaa` 在 `7` 已过期），`renew("bbb", 10)` 生效，`countUnexpiredTokens(15)` → `0`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 哈希表记录过期时刻（`dict`：`tokenId → expireTime`）；设计题里把「状态」归结为一个数。

**一句话。** 只存每个验证码的过期时刻 `currentTime + timeToLive`；`renew` 先判断「过期时刻 > 当前时刻」再延期，`count` 数过期时刻大于当前时刻的项。

**识别。** 带 TTL 的缓存 / 令牌 / 会话 = 存过期时刻而不是创建时刻，判断一次比较搞定；调用上限 `2000` 次，`count` 线性扫描 `O(n)` 完全够用。

**推导。** 不需要定时器去删过期项，过期是**惰性**判断的：每次操作时拿过期时刻与当前时间比较。过期时刻等于当前时间也算过期，所以比较一律是严格的 `过期时刻 > 当前时间`。

```python
class AuthenticationManager:
    def __init__(self, timeToLive: int) -> None:
        self.ttl = timeToLive
        self.expire: dict[str, int] = {}  # tokenId -> 过期时刻；过期的项不删，惰性判断

    def generate(self, tokenId: str, currentTime: int) -> None:
        self.expire[tokenId] = currentTime + self.ttl

    def renew(self, tokenId: str, currentTime: int) -> None:
        # 不存在时取 0（currentTime >= 1），已过期（过期时刻 <= 当前时刻）也不满足：两种情况都忽略
        if self.expire.get(tokenId, 0) > currentTime:
            self.expire[tokenId] = currentTime + self.ttl

    def countUnexpiredTokens(self, currentTime: int) -> int:
        return sum(t > currentTime for t in self.expire.values())
```

运行：示例里两次 `countUnexpiredTokens` 依次返回 `1`、`0`，两次被忽略的 `renew` 不产生任何变化；`generate("a", 2)`（`ttl = 5`）后 `countUnexpiredTokens(7)` → `0`；只做 `renew("x", 1)` 后 `countUnexpiredTokens(2)` → `0`。

**复杂度。** `generate`、`renew` 为 `O(1)`，`countUnexpiredTokens` 为 `O(n)`，空间 `O(n)`。

**拓展优化。**
- 调用次数很大时，`count` 要做到均摊 `O(1)`：时间严格递增，且每次生成或续期的过期时刻都是 `当前时间 + ttl`，所以按「最后更新时间」排序的顺序就是按过期时刻排序的顺序；用 `OrderedDict`，续期时 `move_to_end`，`count` 前从队头弹出过期项：

```python
from collections import OrderedDict


class AuthenticationManagerFast:
    def __init__(self, timeToLive: int) -> None:
        self.ttl = timeToLive
        self.expire: OrderedDict[str, int] = OrderedDict()  # 过期时刻从小到大

    def _purge(self, now: int) -> None:
        while self.expire and next(iter(self.expire.values())) <= now:  # 队头最早过期
            self.expire.popitem(last=False)

    def generate(self, tokenId: str, currentTime: int) -> None:
        self.expire[tokenId] = currentTime + self.ttl

    def renew(self, tokenId: str, currentTime: int) -> None:
        self._purge(currentTime)  # 过期的先清走，剩下的就都是有效的
        if tokenId in self.expire:
            self.expire[tokenId] = currentTime + self.ttl
            self.expire.move_to_end(tokenId)  # 新过期时刻最大，放队尾

    def countUnexpiredTokens(self, currentTime: int) -> int:
        self._purge(currentTime)
        return len(self.expire)
```

**易错点。**
- 比较写成 `>=`：`generate("a", 2)`（`ttl = 5`）后 `countUnexpiredTokens(7)` 返回 `1`，正确是 `0`，因为过期时刻就是 `7`，过期优先。
- `renew` 不判断是否存在或过期、直接赋值：先 `renew("x", 1)` 再 `countUnexpiredTokens(2)` 返回 `1`，正确是 `0`；已过期的验证码也会被「复活」。
- 在 `renew` 里用创建时刻而不是当前时刻重新计时，过期时刻会算错。

**同模式。** LC 146 LRU 缓存、LC 362 敲击计数器、LC 359 日志速率限制器、LC 981 基于时间的键值存储。

---
id: craft-interface-only-when-earned-4-extract-when-third-copy
node: craft.architecture.interface-only-when-earned
type: qa
step: 4
---
## Q
**接口是挣来的 · 同一个限流器写了两份，该抽成共享模块吗**｜架构

通知服务内部自带了一个很小的滑动窗口限流器（`allow(key) -> bool`），独立的限流器题里又有一个带四种算法、返回结构化决策的完整版。两份看上去是重复。什么时候该合并成共享模块？在合并之前，怎么让将来的合并代价很小？

## A
**要点。** 重复便宜、错误抽象昂贵：只有一个使用场景时，抽出去的接口往往是猜的，第二个、第三个使用方一来就被迫改。常用经验是出现第三份相同需求再抽象（rule of three），并且让每个使用方只依赖它需要的最小能力，这样将来换实现只改一行适配代码。

```python
# 小而自带：只有一个算法，allow(key) -> bool
class WindowLimiter:
    def __init__(self, limit: int, window: float, clock: Callable[[], float]) -> None:
        self._limit, self._window, self._clock = limit, window, clock
        self._hits: dict[str, deque[float]] = {}
    def allow(self, key: str) -> bool:
        now, q = self._clock(), self._hits.setdefault(key, deque())
        while q and q[0] <= now - self._window:
            q.popleft()
        if len(q) >= self._limit:
            return False
        q.append(now)
        return True

# 另一处的完整限流器：返回结构化决策
@dataclass(frozen=True)
class Decision:
    allowed: bool
    retry_after: float

class FullLimiter:
    def __init__(self) -> None:
        self.n = 0
    def try_acquire(self, key: str, now: float) -> Decision:
        self.n += 1
        return Decision(self.n <= 2, 0.0 if self.n <= 2 else 5.0)

class Notifier:                               # 只依赖它需要的一个能力
    def __init__(self, allow: Callable[[str], bool]) -> None:
        self._allow = allow
    def send(self, user: str) -> str:
        return "sent" if self._allow(user) else "throttled"

t = [0.0]                                     # 可变的假时钟
small = Notifier(WindowLimiter(2, 10, lambda: t[0]).allow)             # 自带的小版本
full = FullLimiter()                          # try_acquire(key, now) -> Decision
big = Notifier(lambda k: full.try_acquire(k, t[0]).allowed)            # 换成完整版：一行适配器
print([small.send("u") for _ in range(3)])
print([big.send("u") for _ in range(3)])
```

`WindowLimiter` 是自带的小版本，`full` 是返回 `Decision` 的完整版（前两次放行），实际输出：

```
['sent', 'sent', 'throttled']
['sent', 'sent', 'throttled']
```

**为什么。** 两份其实不是同一件东西：小版本只有一个算法、返回布尔，完整版有四种算法、要返回「多久后重试」。强行合并成一个接口，要么小的背着用不到的复杂度，要么大的被削掉能力。

**代价。** 复制的代价是 bug 修两遍（比如「窗口里没人就删掉 key，否则字典只涨不落」这类内存问题要在每份里各修一次）；所以复制只适合边界清楚、很少改的小件，真正会演化的部件一旦出现第三份就该抽。

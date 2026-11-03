---
id: craft-time-types-4-timestamp-as-data
node: craft.idioms.time-types
type: qa
step: 4
---
## Q
**时间类型 · 把整数时间戳当参数传，和注入一个 Clock，各有什么利弊**｜写法

键值存储把 `timestamp` 作为每个方法的第一个参数，类内完全不读时钟；限流器则是构造时注入一个 `clock` 函数。两种让时间可控的办法怎么选？

## A
**要点。** 都是为了让代码不依赖真实时间，测试能确定地重放。**时间作为数据**（timestamp 参数）：调用方决定每个操作发生在何时，类变成纯函数式的状态机，给定同一串（时间，操作）永远得到同一结果，不需要假时钟也不需要 sleep。**注入 Clock**：类自己在需要时读时间，调用方只在构造时换一个时钟，调用接口更简洁。

```python
class KVStore:
    """时间作为数据：每个方法的第一个参数是 timestamp，类内不读任何时钟。"""
    def __init__(self) -> None:
        self._d: dict[str, tuple[str, int | None]] = {}

    def set(self, ts: int, key: str, value: str, ttl: int | None = None) -> None:
        self._d[key] = (value, None if ttl is None else ts + ttl)

    def get(self, ts: int, key: str) -> str | None:
        v = self._d.get(key)
        if v is None or (v[1] is not None and ts >= v[1]):   # 到期时刻本身已过期
            return None
        return v[0]

kv = KVStore()
kv.set(100, "k", "v", ttl=10)
print([kv.get(t, "k") for t in (100, 109, 110, 111)])
# 同一串事件按时间戳回放，结果永远一样：不需要假时钟，不需要 sleep
print(kv.get(109, "k"), kv.get(109, "k") == kv.get(109, "k"))
```

实际输出：

```
['v', 'v', None, None]
v True
```

**选择依据。** 时间戳参数适合时间本身就是业务输入的场景（事件带有发生时间，按日志回放、批处理、面试题要求的接口）；注入 Clock 适合时间是内部实现细节，调用方不该关心（限流器内部读自己的窗口）。

**代价。** 时间作为参数，每个调用都要传，调用方可能传出倒退的时间戳：类要决定是拒绝、容忍还是校正（这里需要写明约定，例如「时间戳不会递减」）。注入 Clock 则在类内部多处读时间，同一个操作里读两次会得到不同的值，一次操作内应只读一次。

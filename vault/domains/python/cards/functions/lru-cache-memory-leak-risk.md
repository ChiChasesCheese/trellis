---
id: lru-cache-memory-leak-risk
node: functions.functools
type: qa
source: python-docs
---
## Q
`@functools.lru_cache` 缓存一个函数存在内存泄漏（memory leak）风险，具体体现在哪？什么样的函数不适合用它缓存？

## A
缓存条目会一直持有参数和返回值的引用，直到该条目被淘汰（超过 `maxsize`）或手动调用 `cache_clear()`；如果 `maxsize=None`，缓存可以无限增长，长期运行的进程（如 Web 服务）会越占越多内存。带副作用的函数、每次调用都要产生新的可变对象（比如生成器、协程函数）、或结果依赖调用时刻的不纯函数（比如 `time.time()`、`random.random()`）都不适合缓存，因为缓存会让它们的行为变得不正确或没有意义。

---
id: craft-composition-of-independent-axes-5-registry-and-config
node: craft.architecture.composition-of-independent-axes
type: qa
step: 5
---
## Q
**独立变化轴的组合 · 配置里写的名字怎么变成对象，新增一种策略要改哪里**｜架构

缓存要能由配置创建：`eviction="lfu"`、`backend="file"`。如果创建函数里写一串 `if eviction == "lru": ... elif ...`，每加一种策略就要改它。在系统层面，Redis 的 `maxmemory-policy` 和可插拔存储引擎也是这个思路吗？

## A
**要点。** 用注册表（名字到构造函数的字典）做翻译层：创建函数只查表，名字不认识就报错并列出已知的选项；新增一种策略只往表里加一行，创建函数不动。这是「轴」的最后一步：轴的实现可以独立增长，配置层只认名字。放大到系统，Redis 的淘汰策略是配置项，存储引擎和中间件栈同样是「选一个实现、插进固定流程」。

```python
class ConfigError(ValueError): ...

class LruPolicy: ...
class LfuPolicy: ...
class MemoryStore: ...
class FileStore:
    def __init__(self, cfg) -> None: self.dir = cfg.directory

@dataclass(frozen=True)
class CacheConfig:
    capacity: int = 100
    eviction: str = "lru"
    backend: str = "memory"
    directory: str | None = None

POLICIES: dict[str, Callable[[], object]] = {"lru": LruPolicy, "lfu": LfuPolicy}
BACKENDS: dict[str, Callable[[CacheConfig], object]] = {
    "memory": lambda cfg: MemoryStore(),
    "file": FileStore,
}

def create_cache(cfg: CacheConfig) -> tuple[object, object]:
    if cfg.eviction not in POLICIES:
        raise ConfigError(f"unknown eviction policy {cfg.eviction!r}; known: {sorted(POLICIES)}")
    if cfg.backend not in BACKENDS:
        raise ConfigError(f"unknown backend {cfg.backend!r}; known: {sorted(BACKENDS)}")
    return POLICIES[cfg.eviction](), BACKENDS[cfg.backend](cfg)

p, s = create_cache(CacheConfig(eviction="lfu", backend="file", directory="/tmp/c"))
print(type(p).__name__, type(s).__name__)
try:
    create_cache(CacheConfig(eviction="fifo"))
except ConfigError as e:
    print(e)

class FifoPolicy: ...
POLICIES["fifo"] = FifoPolicy                      # 新增一种策略：只改注册表
print(type(create_cache(CacheConfig(eviction="fifo"))[0]).__name__)
```

创建 `lfu` 加 `file`；再创建一个未注册的 `fifo`；注册 `FifoPolicy` 后再创建，实际输出：

```
LfuPolicy FileStore
unknown eviction policy 'fifo'; known: ['lfu', 'lru']
FifoPolicy
```

**为什么。** 错误信息里列出已知的名字，配置写错时马上知道可选项；后端的构造函数收整个配置（文件后端要目录），策略的不用，所以两个表的值签名不同，各自按需。

**代价。** 名字是字符串，拼写错误要到运行时才发现，所以要在启动时就创建一次，别等到第一次读写；注册表是全局可变状态，插件式扩展时要考虑注册时机与重名。

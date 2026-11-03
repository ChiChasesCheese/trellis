---
id: craft-init-subclass-registry-5-scales-fail-fast-config
node: craft.idioms.init-subclass-registry
type: qa
step: 5
---
## Q
**__init_subclass__ 注册表 · 从注册表到启动时校验配置和插件发现**｜写法

缓存配置里的 `eviction`、`backend` 是字符串，由注册表翻译成对象。放到真实服务里，配置由运维下发，插件由不同团队提供。名字不对时应该什么时候发现？插件的「显式注册」与「按约定扫描」有什么取舍？

## A
**要点。** 越早发现配置错误越便宜：在服务启动或配置下发时就校验所有名字，并一次报出全部问题，而不是等到某个请求第一次用到才炸。插件发现有两种路径：显式注册（配置里或代码里列出来，可读、可审计，但新增要改清单）与约定扫描（放进某个目录或声明入口点就自动生效，方便扩展，但可能加载了没人预期的东西，也依赖导入）。

```python
from dataclasses import dataclass

class ConfigError(ValueError): ...

POLICIES = {"lru": object, "lfu": object}
BACKENDS = {"memory": object, "file": object}

@dataclass(frozen=True)
class CacheConfig:
    capacity: int
    eviction: str = "lru"
    backend: str = "memory"

def validate(cfg: CacheConfig) -> None:
    errors = []
    if cfg.eviction not in POLICIES:
        errors.append(f"unknown eviction {cfg.eviction!r}; known: {sorted(POLICIES)}")
    if cfg.backend not in BACKENDS:
        errors.append(f"unknown backend {cfg.backend!r}; known: {sorted(BACKENDS)}")
    if errors:
        raise ConfigError("; ".join(errors))      # 启动时一次报全，而不是第一次请求才炸

validate(CacheConfig(100, "lfu"))
try:
    validate(CacheConfig(100, "lruu", "redis"))
except ConfigError as e:
    print("ConfigError:", e)
```

实际输出：

```
ConfigError: unknown eviction 'lruu'; known: ['lfu', 'lru']; unknown backend 'redis'; known: ['file', 'memory']
```

**为什么。** 两个错误一次报出，并且带着可选清单，运维修一次就够。对应到进程内部，是同一个想法：`create_cache` 在装配时查表，名字找不到立刻抛 `ConfigError`，而不是装配出一个半成品。

**取舍。** 配置来自可信的同一个团队：显式清单更安全、更容易审计。需要第三方扩展：约定扫描，但要限制扫描范围、记录加载了哪些插件、对插件做版本和兼容检查。无论哪种，都要保证配置错误不会让线上服务在运行中途才暴露。

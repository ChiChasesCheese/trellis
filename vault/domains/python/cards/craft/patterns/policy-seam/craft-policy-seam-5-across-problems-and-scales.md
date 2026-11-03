---
id: craft-policy-seam-5-across-problems-and-scales
node: craft.patterns.policy-seam
type: qa
step: 5
---
## Q
**策略接缝 · 订座、网约车、自动售货机、缓存、送餐、折扣里的同一个接缝**｜模式

航司超售、网约车加价与匹配、售货机找零、缓存淘汰、送餐机器人分派、折扣叠加。它们各自的接缝长什么样？放大到分布式系统，同一个想法叫什么？

## A
**要点。** 都是：核心流程固定，一个变化点在构造时注入，默认值取下界。形状按规则要不要记账来选，接缝的输入是只读快照、输出是决定。

```python
# airline：单个函数
OverbookingPolicy = Callable[[CabinClass, "FlightInstance"], int]
# ttl-cache：有状态的四方法对象
class EvictionPolicy(Protocol[K]): ...
# amz-discount-engine：不是类，是引擎的枚举参数
class Stacking(Enum): STACK = "stack"; BEST_ONLY = "best_only"
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

**见于。** airline（超售、票价、退票）、ride-sharing（加价、匹配）、vending-machine（找零算法，默认精确背包）、ttl-cache（淘汰）、amz-robot-restaurant（分派）、amz-discount-engine（叠加）。

**不变的。** 默认值是策略的下界（不超售、不加价、不退款）；核心只依赖一个窄接口。**变化的。** 形状（函数 / 对象 / 枚举），以及接缝上的校验强度：像分派这种返回值会驱动动作的接缝，核心要校验策略的输出。

**信号。** 需求里出现「可配置」「不同的客户有不同的规则」「以后可能换成……」「先做个简单的，后面再加」；或者核心函数里堆了越来越多的分支，每个分支对应一个业务方的要求。

**尺度对照。** 低层设计：构造函数里传入的函数或对象。分布式：Redis 的 `maxmemory-policy`（allkeys-lru 等）把淘汰做成配置项；服务的插件接口（SPI）、定价或风控的规则引擎、特性开关。变化：策略不再是同进程里的函数，而是一份可以热更新的配置或远程服务，于是新问题出现了：策略的版本要和被它决定的数据一起记录（否则无法复算当时为什么这样决定），策略失败时核心要有降级的默认值，也就是单机版里「下界」那一行。

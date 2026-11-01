---
id: hi-pt-api-circuit-breaker-2-enum-vs-class
node: points.api-circuit-breaker
type: qa
step: 2
---
## Q
**熔断器 · 状态模式用枚举还是状态类**｜出自：熔断器 › 核心实体与接口

实现熔断器的三种状态时，可以用枚举加条件分支，也可以把每个状态做成一个类（State 模式）。什么时候选哪种？熔断器的降级逻辑应该怎么注入？

## A
**取舍。** 各状态行为差异不大时，枚举加条件分支更直接；每个状态行为复杂时，才把每个状态做成类，把转换逻辑放进状态对象。
**这里的选择。** 枚举，因为只有两处分支：放行判断和结果回报。
**降级。** 用策略（Strategy）注入，即 `call(fn, fallback=None)` 传入回调函数；没有降级回调时抛出 `CircuitOpenError`。

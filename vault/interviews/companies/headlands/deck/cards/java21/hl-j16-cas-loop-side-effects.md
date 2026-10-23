---
id: hl-j16-cas-loop-side-effects
node: java21.j16-concurrency-primitives
type: qa
step: 37
---
## Q
写 CAS 循环时有哪些常见错误？

## A
- **循环里做副作用**：CAS 失败会重试，副作用（打日志、发请求、改别的状态）会被重复执行；循环体应只做纯计算。
- **忽略 ABA**：`compareAndSet` 比较的是引用/值，不是「没人动过」，必要时加版本号。
- **用 `LongAdder.sum()` 做精确判断**：`sum()` 不是快照。
- **以为 `volatile` 能做复合操作**：需要原子读-改-写就用 CAS 家族。

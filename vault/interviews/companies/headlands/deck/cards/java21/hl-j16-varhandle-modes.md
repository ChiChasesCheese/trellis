---
id: hl-j16-varhandle-modes
node: java21.j16-concurrency-primitives
type: qa
step: 14
---
## Q
`VarHandle` 的 plain、opaque、acquire/release、volatile、CAS 家族五种访问模式分别保证什么、用在哪？

## A
| 模式（方法名） | 保证 | 典型用途 |
|---|---|---|
| plain：`get`/`set` | 无额外保证，等价普通字段访问 | 线程内自己的数据 |
| **opaque**：`getOpaque`/`setOpaque` | 单个变量上读写不被撕裂、不被编译器缓存/消除（最终会看到）；**不保证**跨变量顺序 | 自旋等待标志、统计 |
| **acquire/release**：`getAcquire`/`setRelease` | 单向栅栏 | 发布/订阅数据、SPSC 队列 |
| **volatile**：`getVolatile`/`setVolatile` | 完整 `volatile` 语义（顺序一致） | 同 `volatile` 字段 |
| **CAS 家族** | 原子读-改-写：`compareAndSet`、`compareAndExchange`、`weakCompareAndSet*`、`getAndAdd`、`getAndSet`、`getAndBitwiseOr` | 无锁更新 |

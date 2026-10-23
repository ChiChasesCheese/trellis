---
id: hl-j11-policies
node: java21.j11-structured-concurrency
type: qa
step: 6
---
## Q
`StructuredTaskScope` 的策略（policy）由谁决定？内置的 `ShutdownOnFailure` 与 `ShutdownOnSuccess` 各是什么语义、适合什么场景？

## A
作用域基类 `StructuredTaskScope<T>` 的策略由**子类**决定：什么时候算整体完成、失败怎么处理。

- `ShutdownOnFailure`：**任何子任务失败 → 取消其余**。用于「全部成功才有意义」，如下单前并行检查行情 + 风控 + 参考数据。
- `ShutdownOnSuccess<T>`：**第一个成功 → 取消其余**。用于「谁先回用谁」，如对冲请求、同一价格向多个交易所查询择一。

这两个是内置的，都是「一个失败/成功就收工」；其他需求要自己写子类。

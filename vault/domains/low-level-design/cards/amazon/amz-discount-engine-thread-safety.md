---
id: amz-discount-engine-thread-safety
node: amazon.amz-discount-engine
type: qa
step: 8
tags: [grown]
---
## Q
在购物车折扣引擎里，多线程同时往购物车加商品、同时调用 compute 算价，哪里会出竞争？怎么防？

## A
`PriceEngine` 构造后只含元组，`compute` 是纯函数，可被多线程共享，不需要锁。

会竞争的是 `Cart.add` 的读-改-写：「取旧数量、加上新数量、写回」之间线程可以切换，丢更新。GIL 只保证单条字节码原子，不保证这三步原子。用一把 `threading.Lock` 包住 `add` / `remove`，`lines` 在锁内复制成元组。

8 线程各加 200 次后数量应恰好是 1600，`compute` 在快照上工作，不会读到半个修改。

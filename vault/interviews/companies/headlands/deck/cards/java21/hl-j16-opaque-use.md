---
id: hl-j16-opaque-use
node: java21.j16-concurrency-primitives
type: qa
step: 43
---
## Q
`VarHandle` 的 opaque 模式保证什么、不保证什么？适合什么场景？

## A
`getOpaque`/`setOpaque` 保证：单个变量上的读写**不被撕裂、不被编译器缓存或消除**，最终会被看到。

**不保证**跨变量的顺序，所以不能用它发布数据（别的字段的写入可能还不可见）。适合：自旋等待标志、统计这类「只关心这个变量自己最终有值」的场景。需要发布其他数据时用 acquire/release。

---
id: hl-j12-not-replacement
node: java21.j12-scoped-values
type: qa
step: 18
---
## Q
`ScopedValue` 是 `ThreadLocal` 的完全替代吗？各自适合什么场景？

## A
不是完全替代。
- **`ThreadLocal`** 仍适合「**每线程一份、可变、长生命周期**」的东西，如每线程复用的缓冲区、非线程安全的 `SimpleDateFormat`。
- **`ScopedValue`** 解决「**调用链上的只读上下文**」：用户、traceId、事务、截止时间。

更新上下文只能重绑定。「在深层改一个值让上层看到」做不到，那说明你要的是**返回值**，不是上下文。

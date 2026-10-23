---
id: hl-j12-flaw-lifecycle
node: java21.j12-scoped-values
type: qa
step: 2
---
## Q
`ThreadLocal` 的第一个结构性毛病：生命周期不受控。线程池里会出什么事？

## A
`set` 后值活到线程死或手动 `remove()`。线程池复用线程，请求 A 忘了 `remove` 的值，请求 B 在同一线程上读到。

实验：处理 alice 时不清理，下一个请求没 `set` 却读到 `USER=alice`。**在交易系统里就是「用了别人的账户」**，既是泄漏也是串号。

正确用法必须写 `try { USER.set(u); ... } finally { USER.remove(); }`，靠人肉纪律，一旦漏掉就出事。

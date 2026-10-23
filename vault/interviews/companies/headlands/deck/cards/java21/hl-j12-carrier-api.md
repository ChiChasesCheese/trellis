---
id: hl-j12-carrier-api
node: java21.j12-scoped-values
type: qa
step: 7
---
## Q
`ScopedValue.where(...)` 返回什么？`Carrier` 的 `where`、`run`、`call`、`get` 各是什么作用？

## A
`ScopedValue.where(key, value)` 返回一个 `Carrier`（携带者），表示「准备好绑定 key=value」，**还没生效**。

- `Carrier.where(key2, value2)`：链式再绑一个，`where(A, a).where(B, b).run(...)`。
- `Carrier.run(Runnable)`：绑定生效并执行 lambda，结束自动解绑，无返回值。
- `Carrier.call(Callable<R>)`：同上，有返回值，可抛受检异常。
- `Carrier.get(Supplier<R>)`：JDK 21 里的变体，有返回值，不抛受检异常。

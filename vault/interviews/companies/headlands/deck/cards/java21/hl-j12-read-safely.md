---
id: hl-j12-read-safely
node: java21.j12-scoped-values
type: qa
step: 9
---
## Q
`ScopedValue.get()` 在未绑定时会怎样？有哪几种安全的读法？

## A
`key.get()` 未绑定会抛 **`NoSuchElementException`**。

安全读法：
- `key.isBound()`：当前线程现在有没有绑定；
- `key.orElse(default)`：未绑定给默认值；
- `key.orElseThrow(Supplier)`：未绑定抛自定义异常；
- 或者保证所有入口都绑定过。

JDK 25 起 `ScopedValue.orElse` 不再接受 `null` 参数。

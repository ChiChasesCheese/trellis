---
id: hl-j16-varhandle-why
node: java21.j16-concurrency-primitives
type: qa
step: 13
---
## Q
Java 9 的 `VarHandle` 为什么要存在？它相对 `AtomicIntegerFieldUpdater`、`Unsafe`、`volatile` 解决了什么？

## A
- Java 5–8 对**普通字段**做 CAS 只能用 `AtomicIntegerFieldUpdater`（反射，慢，限制多）或 `sun.misc.Unsafe`（私有 API，JDK 在收紧）。
- `volatile` 太「重」：每次读写都是最强的顺序一致（Sequentially Consistent）保证，很多无锁结构只需要更弱更便宜的保证。

`VarHandle` 把「变量」抽象成句柄，提供**不同强度的访问模式**，可作用于字段、数组元素、`byte[]` 视图。

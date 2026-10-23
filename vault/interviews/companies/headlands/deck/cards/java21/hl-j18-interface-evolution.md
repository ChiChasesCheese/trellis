---
id: hl-j18-interface-evolution
node: java21.j18-comparators-interfaces
type: qa
step: 4
---
## Q
Java 7 的接口为什么很难演进？Java 8、9 分别加了什么来解决？

## A
Java 7 接口里所有方法都是抽象的。给 `Iterable` 加个 `forEach`，世界上所有实现 `Iterable` 的类都会**编译失败**。所以 `Collection` 几乎不能演进，JDK 只能把工具方法放进工具类（`Collections.sort(list)` 而不是 `list.sort()`），静态方法与对象分离、不能被覆盖、也不多态。

- **Java 8**：接口可以有带实现的方法，`default` 方法（给已有实现一个默认实现）和 `static` 方法；`Iterable.forEach`、`List.sort`、`Comparator.reversed()` 就是这样加进去的。
- **Java 9**：接口 `private` 方法，接口内部复用代码。

---
id: hl-j09-compat-and-stream
node: java21.j09-sequenced-collections
type: qa
step: 31
---
## Q
业务类实现 `List` 并自带 `getFirst` / `getLast` / `reversed`，升级到 Java 21 为什么可能编译错误？`stream.toList()` 在 21 里多了什么便利？

## A
给 `List` 等**已有接口**加方法，理论上可能与使用者的类冲突（如自己有个不同返回类型的 `reversed()`，或同时实现 `List` 和 `Deque`）。JDK 自己的类（如 `LinkedList`）已处理；业务类升级到 21 后的编译错误就是这个原因。

便利：`stream.toList()` 返回的不可修改 `List` 现在有了 `getFirst` / `getLast` / `reversed`，`stream.toList().getLast()` 比 `list.get(list.size() - 1)` 简洁。

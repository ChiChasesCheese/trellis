---
id: hl-j09-default-methods
node: java21.j09-sequenced-collections
type: qa
step: 16
---
## Q
Sequenced Collections 在编译器和 JVM 层做了什么改动？`SequencedCollection` 里哪个方法是 abstract？这样设计对已有的第三方实现类有什么好处？

## A
**编译器和 JVM 什么都没改**，纯 JDK 库变化：新增接口，给老接口加 `default` 方法，给部分类写高效实现。

`SequencedCollection` 里只有 `reversed()` 是 abstract，`addFirst` / `addLast` / `getFirst` / `getLast` / `removeFirst` / `removeLast` 都是 `default`。

好处：已有的第三方实现类**不用改也能编译运行**。自己写的 `class MyList implements List<X>` 升级到 21 后自动有 `getFirst()`（默认实现：空则抛 `NoSuchElementException`，否则 `get(0)`）。`reversed()` 虽是 abstract，但 `List`、`Deque`、`SortedSet` 等已各给了 `default` 实现（通用反向视图包装类）。

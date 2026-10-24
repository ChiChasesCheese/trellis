---
id: pl-abstraction-equality-hashing-mechanism
node: abstraction.equality-hashing
type: qa
step: 6
---
## Q
哈希表查找一个键的过程是什么？为什么键在放进去之后改了字段，就再也找不到它？

## A
查找分两步：

1. **算哈希**：`hash(key)` 决定桶的位置（或开放寻址的起点）。
2. **比相等**：在该位置逐个比较存着的键，`equals` 为真才算命中。

插入时用的是当时的哈希；之后查找依赖「键的哈希不变」。如果键是可变对象，插入后改了会影响哈希的字段，它还躺在旧哈希对应的桶里，新的查找却去新哈希的桶里找，两边对不上：

```java
Key k = new Key(1);       // hashCode() 返回 id
map.put(k, "v");
k.id = 2;                 // 改了参与哈希的字段
map.get(k)                // null：去 id=2 的桶找
map.get(new Key(1))       // null：到了 id=1 的桶，但 equals 判断 id 不等
map.size()                // 1：条目还在，却没人拿得到
```

条目没有丢，只是成了永远取不回来的「幽灵」，还占着内存。

这解释了各语言的防护：C++ 的 `set`、`unordered_map` 把键存成 `const`，通过迭代器就地改键是编译错误（本机实测 `it->push_back('x')` 报 `has type 'const value_type'`），要改只能删了重插；Python 让可变内置容器不可哈希；Rust 通过所有权让你很难在键被借用时修改它；Java 没有防护，靠约定「键必须是不可变的」（`String`、`Integer`、`record` 的不可变字段）。

契约的第二面是**质量**：哈希要分散，否则退化成链表。Java 的 `HashMap` 在一个桶里链表过长时转成红黑树（Java 8 起），把最坏情况从 O(n) 压到 O(log n)，但这只是兜底；写 `hashCode` 返回常量虽然合法，性能会塌。

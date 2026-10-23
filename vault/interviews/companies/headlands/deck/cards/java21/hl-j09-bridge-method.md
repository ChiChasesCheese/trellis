---
id: hl-j09-bridge-method
node: java21.j09-sequenced-collections
type: qa
step: 18
---
## Q
`javap java.util.List` 为什么能看到两行 `reversed()`？桥方法（bridge method）是什么？

## A
```
public default java.util.List<E> reversed();                 // 新签名（协变返回 List）
public default java.util.SequencedCollection reversed();     // 编译器生成的桥方法，返回类型是父接口的
```
**桥方法**是协变返回类型的实现机制：子接口收窄了返回类型（`List` 比 `SequencedCollection` 窄），为保持二进制兼容父接口签名，编译器额外生成一个转发方法。

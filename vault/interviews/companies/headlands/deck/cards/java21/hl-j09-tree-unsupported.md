---
id: hl-j09-tree-unsupported
node: java21.j09-sequenced-collections
type: qa
step: 14
---
## Q
`TreeSet` / `TreeMap` 上哪些 Sequenced 方法可用，哪些抛异常？为什么？

## A
- **可用**：读（`getFirst`、`getLast`、`firstEntry`、`reversed`）和删除（`removeFirst`、`pollFirstEntry`）。
- **抛 `UnsupportedOperationException`**：`addFirst` / `addLast` / `putFirst` / `putLast`。

原因：位置由比较器决定，不能指定在头 / 尾添加。

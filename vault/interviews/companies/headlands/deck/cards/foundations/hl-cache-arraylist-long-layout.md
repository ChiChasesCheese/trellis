---
id: hl-cache-arraylist-long-layout
node: foundations.cpu-cache-locality
type: qa
step: 14
---
## Q
`ArrayList<Long>` 在内存里每个元素占多少字节？比 `long[]` 多多少？

## A
`ArrayList` 的 `elementData` 是 `Object[]` 引用数组，开启压缩指针时每个引用 **4 字节**；每个 `Long` 是堆上独立对象：12 字节头（8 B mark word + 4 B 压缩类指针）+ 4 字节填充（让 8 字节 `long` 对齐）+ 8 字节值 = **24 字节**。

合计每元素 **28 字节**，实测 28.2 B 对 `long[]` 的 8.2 B，内存约 **3.4 倍**，同样大小的缓存只能装下 `long[]` 的 1/3.4 个元素。

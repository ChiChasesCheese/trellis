---
id: hl-c12-cache-locality-def
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 13
---
## Q
面试问：什么是缓存局部性（cache locality）？为什么 `vector` 遍历比 `list` 快？
Interview question: What is cache locality?

## A
- **时间局部性**：刚访问过的数据很快会再次访问；**空间局部性**：相邻的数据会一起被访问。
- CPU 以**缓存行**（通常 64 字节）为单位读，并**预取**顺序访问的数据。
- `vector` 元素连续，一条缓存行装多个元素且可预取；`list` 节点散落在堆里，每步指针追逐是一次缓存未命中，无法预取。
- 数字参考：连续 `vector<Order>` 比乱序指针数组快约 9 倍。

---
id: hl-cq-q16-padding-offsetof-empty
node: cpp-questions.c-memory-ownership
type: qa
step: 32
---
## Q
三个追问：编译器为什么填充而不是紧密打包？`offsetof` 是什么？空类的 `sizeof` 是多少？

## A
- **为什么填充**：未对齐的加载在有些 CPU 上更慢甚至会出错，而且原子操作需要对齐。
- **`offsetof`**：给出成员的字节偏移（对 standard-layout 类型有效），可用来打印布局。
- **空类**：`sizeof` 是 **1** 字节；作为基类时，**空基类优化**（empty base optimization）让它占 0 字节。

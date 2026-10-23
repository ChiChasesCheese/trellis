---
id: hl-javaq-d-q12-semantics
node: java-questions.d-memory
type: qa
step: 7
---
## Q
`System.arraycopy(src, sp, dst, dp, len)` 在重叠拷贝、越界、类型不兼容时各有什么行为？JIT 怎么处理它？

## A
- **重叠**：语义等同 memmove，同一数组内重叠拷贝也正确。例：`[1..6]` 从 0 拷到 2、len=4，结果 `[1, 2, 1, 2, 3, 4]`。
- **越界**：抛 `ArrayIndexOutOfBoundsException`（如 `last destination index 9 out of bounds for int[6]`）。
- **引用数组元素类型不兼容**：抛 `ArrayStoreException`。
- **JIT**：被当作 intrinsic，小拷贝内联成几条向量指令，大拷贝调用优化过的 stub；16 个 long 的 arraycopy + 读写约 **1.7 ns/次**。
- `Arrays.copyOf(a, n)` = 分配新数组（清零）+ arraycopy。

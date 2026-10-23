---
id: hl-javaq-rubric-d-memory
node: java-questions.rubric
type: qa
step: 7
---
## Q
回答"分配、对象大小、装箱、字符串、堆外、缓存"这类内存问题，强、一般、弱的答案各有什么特征？

## A
- **强**：`new` = TLAB 指针碰撞 + 清零 + 构造，代价后移到 GC，逃逸分析可消除；对象头 12 字节 + 8 字节对齐，能心算 `Integer`=16、`int[10]`=56，`ArrayList<Integer>` ≈ 5 倍于 `int[]`；`Integer` 缓存与 `==`；`String` 不可变 / 紧凑 / 缓存 hash / 循环拼接 O(n²)；堆外的收益与风险（生命周期、限制、不可见）；缓存行与伪共享，能说"顺序遍历 vs 追指针"约一个数量级；`System.arraycopy` 是 memmove 语义，稳态下手写循环可能被优化成同样的东西，但仍优先 arraycopy。
- **一般**：知道 `new` 在堆上、有 GC，知道装箱有开销但不会量化；知道 `StringBuilder`。
- **弱**：把 C++ 的 `malloc` / `new` 机制原样套到 Java；说 `substring` 共享底层数组（那是 Java 6 的行为）；不知道缓存行。

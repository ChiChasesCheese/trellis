---
id: hl-javaq-a-q02-table
node: java-questions.a-speed
type: qa
step: 6
---
## Q
从"值类型/内联布局、边界检查、泛型实现、未定义行为、多态调用"几个维度，对比 C++、Rust、Go、Java（HotSpot）的运行时代价。

## A
- **值类型 / 内联布局**：C++、Rust、Go 都有（struct 成员可内联）；Java 21 **没有**（Valhalla 未发布），除原始类型外都是堆对象加引用。
- **数组边界检查**：C++ 默认无；Rust 默认有但可被优化掉；Go 有；Java 有，但 JIT 常消除。
- **泛型实现**：C++ 模板按类型展开；Rust 单态化（monomorphization）；Go 是字典与展开混合；Java 是**擦除**，容器里装引用（装箱）。
- **未定义行为**：C++ 有，优化器可利用；Rust 无（`unsafe` 除外）；Go 和 Java 无（Java 的数据竞争也有定义的弱语义）。
- **多态调用**：C++ 默认非虚；Rust 的 trait 默认静态分发；Go 是接口间接调用；Java 默认虚调用，由 JIT 去虚化。
- **编译时机**：C++/Rust/Go 是 AOT，Java 是 JIT；**内存回收**：C++ 手动或 RAII，Rust 用编译期所有权，Go/Java 用 GC。

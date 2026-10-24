---
id: pl-abstraction-generics-implementation-unique-erasure-vs-reified
node: abstraction.generics-implementation
type: qa
step: 7
---
## Q
Java 的擦除和 C# 的具化泛型（reified generics）是同一个问题的两个答案。它们各自揭示了怎样的取舍？

## A
**C#**（2005，.NET 2.0）选择具化：运行期保留完整类型信息。`List<int>` 与 `List<string>` 是不同的运行期类型，JIT 对值类型实参生成专用代码（`List<int>` 里存的是裸 `int`，无装箱），对引用类型实参共享一份代码。因此 `typeof(T)`、`new T()`、`x is List<string>` 都可以。代价：.NET 当年**打破了与旧集合库的二进制兼容**，旧的 `ArrayList` 保留，新的 `List<T>` 另起一套。

**Java** 在 2004 年选择擦除：新旧代码二进制兼容，旧库无需重新编译。代价就是后来二十年的各种限制：不能 `new T()`、不能 `instanceof List<String>`、基本类型要装箱。

取舍的核心是**谁来承担迁移成本**：C# 让生态一次痛，换来干净的语义；Java 让每个使用者每天都痛一点，换来没有断裂。Java 平台后来的 Valhalla 项目试图补上这块短板：让泛型能直接对值类型特化，减少装箱，同时保持兼容，这说明擦除的限制被认为足够痛、值得做大规模修复。

Go 的方案吸收了两者：值类型专用、指针共享，无需破坏兼容，因为它在泛型诞生时没有旧代码负担。这是「晚加入」的优势。

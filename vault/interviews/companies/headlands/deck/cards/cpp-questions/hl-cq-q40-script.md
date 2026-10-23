---
id: hl-cq-q40-script
node: cpp-questions.j-cross-language
type: qa
step: 8
---
## Q
用英文 60 秒回答：You use Java every day. What are the main differences between Java and C++?

## A
结构：谁负责安全与内存（堆+GC 对值+RAII+UB）→ 泛型擦除对模板实例化 → 小差别（`final` 对 `const`、默认非虚、构建模型、`volatile`）→ 习惯直译（try-with-resources 变成作用域，`synchronized` 变成 `lock_guard`，`Optional` 变成 `std::optional`）。

- The biggest difference is **who owns safety and memory**. In Java objects live on the heap behind references and the GC reclaims them; arithmetic and bounds are defined. In C++ an object is a **value** - on the stack, inline in another object, contiguous in a vector - lifetime is deterministic via **RAII**, and many mistakes, such as out-of-bounds or signed overflow, are **undefined behavior**.
- Generics versus templates: Java erases and boxes; C++ instantiates per type, so `vector<int>` holds real ints.
- Smaller things: `final` fixes a reference while `const` constrains the object; methods are non-virtual by default; the build model is headers and a linker rather than classpath; and `volatile` means something different - in C++ it's not synchronization.
- I map idioms directly: try-with-resources becomes a scope, `synchronized` a `lock_guard`, `Optional` a `std::optional`.

---
id: hl-cq-q20-script
node: cpp-questions.e-templates
type: qa
step: 5
---
## Q
用英文 60 秒回答：How do C++ templates differ from Java generics? What are concepts and SFINAE?

## A
结构：Java 擦除装箱 vs C++ 按类型实例化 → 代价（膨胀、编译慢、只在实例化时检查）→ concepts 把错误挪到调用处，之前用 SFINAE/`enable_if` → 非类型参数。

- Java generics use **type erasure**: one compiled body, containers hold references, primitives get boxed. C++ templates are **compile-time code generation**: every type used gets its own instantiation, so `vector<int>` holds real ints with **no boxing** and the compiler can inline everything.
- The costs are **code bloat**, longer compile times, and the fact that a template body is only checked when instantiated - historically giving page-long errors.
- **Concepts** in C++20 fix that: I state requirements like "has a `price()` returning something convertible to double", and a wrong type fails at the call site with a one-line reason. Before concepts that was done with **SFINAE** and `enable_if`.
- Templates also take non-type parameters - `std::array<int, 16>` - which Java can't.

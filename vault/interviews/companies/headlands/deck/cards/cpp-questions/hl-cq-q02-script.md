---
id: hl-cq-q02-script
node: cpp-questions.a-why-fast
type: qa
step: 11
---
## Q
用英文 60 秒回答：Why is C++ faster than other compiled languages (Rust, Go, Java with AOT)?

## A
结构：编译本身不决定速度 → 剩余运行时工作与布局控制 → C++ 连续布局可见 → Java 靠 JIT 追回但布局是结构性差距 → 对 Rust 只差生态。

- Compiling is not what makes code fast; what matters is **how much runtime work is left** and **how much control I have over memory**.
- C++ and Rust pay only for what you use. Java and Go have a **garbage collector**, and in Java everything except primitives is a heap object behind a reference - a list of orders is a list of pointers, so scanning it **chases pointers** instead of reading sequentially.
- In C++ a vector of structs is one **contiguous block**; I can see it: consecutive elements are exactly `sizeof(Order)` apart.
- Java gets some of that back with **JIT** optimizations a static compiler cannot do, and value types are coming, but today layout is the structural gap.
- Against Rust, machine code quality is similar - same LLVM backend; the difference is ecosystem and decades of tooling, not speed.

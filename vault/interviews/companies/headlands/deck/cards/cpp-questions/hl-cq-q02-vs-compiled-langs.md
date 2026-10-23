---
id: hl-cq-q02-vs-compiled-langs
node: cpp-questions.a-why-fast
type: qa
step: 7
---
## Q
面试题：为什么 C++ 比其他编译型语言（Rust、Go、带 AOT 的 Java）更快？
Why is C++ faster than other compiled languages (Rust, Go, Java with AOT)?

## A
一句话：不是“编译了就快”，而是**编译之后还剩多少运行时工作、你对内存布局有多少控制权**。

- C++ 和 Rust 把成本设计成“用才付费”；Go、Java 默认带 GC，Java 还有对象头。
- 决定速度的几项：内存回收（C++/Rust 靠 RAII/所有权，Go/Java 靠 GC）；值类型能否内联进数组和对象（C++/Rust/Go 可以，Java 除原始类型外都是堆对象加引用）；数组边界检查（C++ 默认没有）；泛型实现（C++ 模板按类型展开，Java 擦除并装箱）。
- 对 Rust：机器码质量相近（同一个 LLVM 后端），差别是成熟度和生态，不是速度。

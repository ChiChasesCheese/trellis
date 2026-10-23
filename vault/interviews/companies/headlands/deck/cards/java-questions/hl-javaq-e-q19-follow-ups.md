---
id: hl-javaq-e-q19-follow-ups
node: java-questions.e-jit-gc
type: qa
step: 8
---
## Q
追问：热路径上怎么重构代码来避开 megamorphic 调用？lambda 调用会被内联吗？C++ 里对应的情况是什么？
How would you restructure code to avoid a megamorphic call on the hot path? Does a lambda call get inlined?

## A
- **避开 megamorphic**：按事件类型拆分处理循环，让每个调用点只见到少量类型；把热路径特化成 `final` 类 / 单一实现；或在调用者里用 `switch` 分派（`sealed` + 模式 `switch` 走 `invokedynamic` typeSwitch，不一定更快，要测）。
- **lambda**：lambda 是 `invokedynamic` 生成的类；调用点见到的 lambda 种类少时可内联；多种 lambda 经过同一个 `Function.apply` 调用点同样会 megamorphic。
- **对比 C++**：模板在编译期单态化并内联；`virtual` 调用除非编译器能证明具体类型，或用 PGO / LTO 做 devirtualization，否则不能内联。Java 是在**运行时**根据实际观察到的类型做。

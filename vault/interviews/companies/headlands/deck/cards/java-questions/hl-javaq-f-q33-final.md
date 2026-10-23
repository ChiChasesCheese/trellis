---
id: hl-javaq-f-q33-final
node: java-questions.f-concurrency
type: qa
step: 29
---
## Q
`final` 字段的内存语义（JLS 17.5）是什么？什么会破坏它？`record` 一定线程安全吗？
Is a `record` always thread-safe?

## A
- **语义**：只要构造器里没有让 `this` 逃逸，其他线程通过引用读到的所有 final 字段（及它们可达对象在构造器结束时的状态）都是构造完成后的值。
- 所以**不可变对象天然线程安全**，`record`（字段全 final）适合在线程间传递事件。
- **陷阱**：`this` 逃逸（构造器里注册监听器、启动线程）；用普通字段发布可变对象。`HashMap` 放好后不再修改，并通过 volatile / final 发布，读取是安全的（"有效不可变"）。
- **`record` 不一定安全**：字段是 final，但若组件是可变对象（如 `List`），仍需防御性拷贝或不可变集合。

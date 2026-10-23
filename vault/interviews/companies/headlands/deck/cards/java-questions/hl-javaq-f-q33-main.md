---
id: hl-javaq-f-q33-main
node: java-questions.f-concurrency
type: qa
step: 27
---
## Q
什么是安全发布（safe publication）？为什么没有 `volatile` 的双重检查锁（DCL）是坏的？`final` 字段保证什么？
What is safe publication? Why is double-checked locking broken without `volatile`? What do `final` fields guarantee?

## A
一句话：对象构造完成后，如果通过**数据竞争**（无同步）发布引用，别的线程可能看到引用却看到**未初始化完的字段**（重排）。

- **安全发布方式**：volatile 字段、`final` 字段、静态初始化器、持锁发布、线程安全容器。
- **DCL 为何坏**：`new Foo()` 可拆成 1 分配、2 把引用写给 `inst`、3 执行构造器；重排成 1、2、3 后，另一线程看到 `inst != null` 却读到没构造完的对象。
- **修复**：`inst` 声明为 `volatile`。
- **`final` 字段**：构造器结束时有"冻结"保证，其他线程看到引用就保证看到 final 字段的值。

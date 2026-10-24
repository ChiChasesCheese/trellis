---
id: pl-cpp-raii-ownership-found-weak-ptr-cycles
node: cpp.raii-ownership
type: qa
step: 6
---
## Q
`std::weak_ptr` 是什么？引用计数为什么会因为循环引用而泄漏，`weak_ptr` 怎样打破它？

## A
**`weak_ptr`**：指向 `shared_ptr` 所管对象的**非拥有**观察者。它不增加强引用计数，所以不会阻止对象被释放。要使用对象，先调用 `lock()` 得到一个 `shared_ptr`：对象还活着，就得到非空指针；已经释放，就得到空指针。`expired()` 可查询是否已释放。

**循环引用泄漏**：引用计数只在计数归零时释放。如果 A 持有 B 的 `shared_ptr`，B 也持有 A 的 `shared_ptr`，即使外部都不再引用它们，A 和 B 的计数各为 1，永不归零。

```cpp
struct A { std::shared_ptr<A> peer; ~A() { println("A destroyed"); } };
{ auto x = std::make_shared<A>(); auto y = std::make_shared<A>();
  x->peer = y; y->peer = x; }
println("cycle scope ended");
```

实测：作用域结束后**没有**打印 `A destroyed`，两个对象泄漏。把成员换成 `std::weak_ptr<B> peer` 后，同样的结构打印两次 `B destroyed`。

**修法**：设计所有权的**方向**。有明确"父→子"关系时，父拥有子（`shared_ptr` 或 `unique_ptr`），子对父用 `weak_ptr` 或裸指针。典型：树的节点指向父节点用 `weak_ptr`；观察者模式里，被观察者持有观察者的 `weak_ptr`。

**用法与成本**：
- `lock()` 是线程安全的原子操作：成功时增加强计数。
- `weak_ptr` 自身也持有控制块，所以控制块要等强弱计数都归零才释放。

**对比其他语言**：Java 和 Go 的 GC 能识别并回收环，所以没有这个问题；Python 的 CPython 用引用计数，另有周期性的循环垃圾收集器兜底；Rust 的 `Rc` 与 C++ `shared_ptr` 一样会因环泄漏，同样用 `Weak` 解决。C++ 与 Rust 的设计哲学相同：不加运行时环检测，由程序员设计所有权方向。

**要记住的一点**：用了 `shared_ptr`，就要画出所有权图，确认它是**有向无环**的。

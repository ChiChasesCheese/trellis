---
id: pl-cpp-raii-ownership-found-unique-ptr
node: cpp.raii-ownership
type: qa
step: 4
---
## Q
`std::unique_ptr` 是什么？它怎样保证独占所有权，成本有多大？

## A
`std::unique_ptr<T>` 是一个**拥有**堆上 `T` 对象的智能指针（smart pointer，有析构函数的指针包装对象）。它的规则只有两条：
1. 同一时刻只有一个 `unique_ptr` 拥有这个对象。
2. 它析构时 `delete` 所指对象。

**独占靠"只能移动，不能拷贝"实现**：拷贝构造函数被删除，只有移动构造函数。想转让所有权，必须显式 `std::move`。

```cpp
auto p = std::make_unique<int>(1);
auto q = p;              // 编译错误
auto r = std::move(p);   // OK：r 拥有，p 变成空
```

真实报错：`call to implicitly-deleted copy constructor of 'unique_ptr<int>'`。移动后 `p == nullptr`，这是标准**明确保证**的。

**成本**：本机实测 `sizeof(std::unique_ptr<int>)` 为 8 字节，与裸指针相同；解引用就是指针解引用，没有计数器、没有原子操作。使用默认删除器时，它在汇编里与手写 `new`/`delete` 等价，这是"零开销"的典型例子。唯一的额外成本是：对象析构时多一次判断指针是否非空。

**能做什么**：
- `std::make_unique<T>(args...)` 创建，不写 `new`。
- 管数组：`std::unique_ptr<int[]>`。
- 自定义删除器：管理 `FILE*`、C 库句柄，让任何"需要某个函数来关闭"的资源也能用 RAII。
- 作为返回值：`std::unique_ptr<Widget> make()`，调用者得到所有权；作为工厂函数返回多态对象。
- 作为类成员：表达"这个类拥有它"，类自动变成只能移动。

**与 Rust 的关系**：`unique_ptr` 约等于 Rust 的 `Box<T>`，区别是 Rust 的借用检查器**保证**你不会在移动后使用，C++ 只是把指针置空，使用空指针是运行时崩溃。

**要记住的一点**：默认选 `unique_ptr`。只有确实需要多个所有者时，才升级到 `shared_ptr`。

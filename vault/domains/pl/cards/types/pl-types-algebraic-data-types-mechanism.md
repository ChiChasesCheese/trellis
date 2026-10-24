---
id: pl-types-algebraic-data-types-mechanism
node: types.algebraic-data-types
type: qa
step: 6
---
## Q
和类型在内存里是怎么存的？编译器是怎么做到「检查你处理了所有变体」的？

## A
Rust 的 `enum` 是带标签的联合体（tagged union）：一个标签（tag）记录当前是哪个变体，加一块足够放下最大变体的空间，各变体的数据共用这块空间。

```rust
enum Shape { Circle(f64), Rect(f64, f64), Tri(f64, f64, f64) }
// size_of::<Shape>() == 32
```

实际 `size_of::<Shape>()` 是 32 字节：标签对齐后 8 字节，加最大变体 `Tri` 的 3 个 `f64` 共 24 字节。无论当前是圆还是三角形，大小都一样，不需要堆分配。

C++ 的 `std::variant` 是同样的布局：标签加最大成员的空间，无堆分配。
```cpp
using Shape = std::variant<Circle, Rect, Tri>;   // Tri has three doubles
std::visit(overloaded{ /* lambdas for Circle and Rect only */ }, s);
// sizeof(Shape) = 32;  the missing Tri lambda does not compile
```
本机 `clang++ -std=c++23` 实测 `sizeof(Shape)` 是 32，与 Rust 的 `Shape` 完全一样；少写 `Tri` 的 lambda，编译失败并提示 `std::visit requires the visitor to be exhaustive`。（`overloaded` 是把多个 lambda 合并成一个访问者的常见辅助类。）
Java 的 `sealed interface` 加 `record` 则是另一种实现：每个变体是一个独立的类，实例在堆上，对象头里的类指针起标签作用。`sealed` 的关键是 `permits` 子句：编译器知道这个接口的实现类只有列出的几个。

穷尽检查（exhaustiveness check）就建立在这个「集合封闭」的事实上：`match`（Rust）或 `switch`（Java）展开成对每个变体的分支，编译器把变体集合和已写分支做差集，剩下的就是漏掉的。漏了一个就是编译错误：

```console
error[E0004]: non-exhaustive patterns: `&Shape::Tri(_, _, _)` not covered
```

如果类型集合是开放的（普通的接口、可以随意继承的类），编译器不知道所有可能的实现，就无法做这个检查，所以穷尽检查依赖于封闭的和类型。

---
id: pl-types-inference-mechanism
node: types.inference
type: qa
step: 5
---
## Q
Rust 编译器是怎样根据后面的使用反推出 `let mut v = Vec::new();` 的元素类型的？为什么 Go 和 Java 做不到？

## A
Rust 把未知类型当成「类型变量」，边读代码边收集约束，最后求解（统一，unification）。

```rust
let mut v = Vec::new();
v.push(1u8);
println!("{}", std::any::type_name_of_val(&v));
```

推导过程：

1. `Vec::new()` 的类型是 `Vec<T>`，`T` 未知，记为 `?T`，于是 `v: Vec<?T>`。
2. `v.push(1u8)` 要求实参类型等于元素类型，`1u8` 是 `u8`，得到约束 `?T = u8`。
3. 求解完成，`v: Vec<u8>`。

实际输出 `alloc::vec::Vec<u8>`。信息是倒着流的：类型来自后面的使用，而不是初始化那一行。如果整段代码没有任何约束，`?T` 无解，编译器报错：

```console
error[E0282]: type annotations needed for `Vec<_>`
```

所以类型推断不是魔法，而是约束求解：约束够就唯一确定，不够就要求你补标注。

Go 和 Java 的推导是单向的，只看右边的初始化表达式，处理的是「已知量」，不处理「未知量」，因此实现简单、速度快、报错位置就在那一行。C++ 的 `auto`（按初始值推导类型）和模板实参推导（按调用实参推导模板的类型参数）也是单向的：只看初始化表达式或调用的实参，`std::vector v;` 不给元素就推不出，要写 `std::vector<int> v;`。代价是它们做不到这种倒着流的推导：Java 的 `new ArrayList<>()` 没有目标类型时只能退化成 `ArrayList<Object>`。

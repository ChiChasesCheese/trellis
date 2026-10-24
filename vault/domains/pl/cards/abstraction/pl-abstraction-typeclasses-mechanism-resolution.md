---
id: pl-abstraction-typeclasses-mechanism-resolution
node: abstraction.typeclasses
type: qa
step: 7
---
## Q
类型类约束在编译后变成了什么？字典传递、单态化、虚表三种实现各自的成本是什么，什么时候选哪种？

## A
带约束的函数 `max_of<T: Ord>(a, b)` 需要在运行时用到「`T` 怎样比较」。有三种实现方式，区别只是**实例信息在何时、以什么形式存在**。

用同一个功能的两种写法看对应关系：

```java
// the "dictionary" is an ordinary argument
static <T> T maxOf(T a, T b, Comparator<T> ord) { return ord.compare(a, b) >= 0 ? a : b; }
```

```rust
// the compiler finds the Ord instance for the concrete type
fn max_of<T: Ord>(a: T, b: T) -> T { if a >= b { a } else { b } }
```

两个版本对 `3, 7` 都给出 `7`，对 `"pear"`、`"fig"` 给出 `pear`（Java 版用按长度比较的 `Comparator`，Rust 版用字符串的字典序，结果碰巧相同）。

**1. 字典传递**（Haskell 的默认实现，Java 的 `Comparator` 参数是手工版）：函数只编译一份，每次调用多传一个指向实例的指针；方法调用是间接调用。成本：一次间接调用，不能内联；好处：代码体积小，可以多态递归（递归时换类型）。

**2. 单态化**（Rust 的泛型）：对每个具体类型编译一份函数副本，实例的方法被直接内联进去。成本：代码体积随类型数量增加，编译变慢；好处：零运行时开销，优化器看到完整代码。

**3. 虚表**（Rust 的 `dyn Trait`、Java 的虚方法）：数据旁边带指向实例的指针（Rust 在引用里，Java 在对象头里），运行时才选实现。成本：一次间接调用，对象需要统一的表示；好处：可以把不同类型放进同一个集合，二进制体积小。

选择规则：

1. 性能关键、类型数量有限：单态化（Rust 泛型）。
2. 需要异构集合或插件，或编译时间和体积敏感：虚表 / 字典（`dyn Trait`）。
3. 在没有类型类的语言里，显式传 `Comparator` 就是你能得到的最接近的东西，代价是调用者每次都要传，而且容易传错。

C++ 的模板属于第 2 种：重载决议与特化都在编译期完成，实例化后成了直接调用，可以内联；`virtual` 属于第 3 种。
Haskell 的 GHC 在优化时也会对常见类型**特化**（specialise），把字典传递变成类似单态化的代码，说明这是同一概念的两种实现，而不是两种语义。

---
id: pl-functional-first-class-functions-unique-rust-closure-per-type
node: functional.first-class-functions
type: qa
step: 8
---
## Q
Java 把 lambda 塞进具名接口，Rust 给每个闭包一个独特类型。两个选择各自揭示了怎样的价值观？

## A
**Java**：函数是**对象的特例**。语言的类型系统里只有类和接口，所以要引入函数，最小的改动就是让 lambda 成为接口的实例。好处：不引入新的类型种类，旧代码零成本升级，所有工具（反射、序列化、调试器）照旧工作。代价：函数的类型信息被接口名取代（`Function` 还是 `UnaryOperator` 还是自定义接口，三个等价的东西互不兼容）；泛型无法用于基本类型，所以有 `IntFunction`、`ToLongFunction` 等一大堆特化接口。

**Rust**：函数是**编译期的静态代码**。闭包的捕获方式、大小、调用约定都写进类型里，编译器据此在编译期完全展开。好处：`iter.map(|x| x + 1)` 编译后和手写循环一模一样。代价：类型无法写出名字（只能用 `impl Fn` 或泛型 `F`），装进集合或返回不同分支需要 `Box<dyn Fn>`，也就是主动付动态分派的代价。

这两个选择对应的是两种世界观：Java 想让**生态保持连续**，用最小的变动融入函数式；Rust 想让**抽象不付代价**，宁可让类型系统更复杂，也要让编译器看清一切。

对比点：Java 在运行期通过 JIT 才能恢复被抹掉的信息（把 lambda 内联），Rust 在编译期就保留了全部信息。同样的 `list.stream().map(x -> x + 1)`，Java 靠 JIT 预热后才接近 Rust 的速度，Rust 一开始就是。

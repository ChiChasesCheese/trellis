---
id: pl-abstraction-dispatch-mechanism
node: abstraction.dispatch
type: qa
step: 5
---
## Q
Rust 的泛型调用与 `dyn Trait` 调用在机器层面有什么不同？Go 的接口调用又处在哪个位置？

## A
同一个 trait 方法，两种写法：

```rust
fn stat<T: Shape>(x: &T) -> f64 { x.area() }   // 泛型：静态分派
fn dynm(x: &dyn Shape) -> f64 { x.area() }     // trait 对象：动态分派
```

- **泛型**：编译器为每个实际类型各生成一份 `stat`（单态化，详见泛型实现一节），调用是直接 `call`，常常被内联。代价是每多一种类型就多一份机器码。
- **`dyn Trait`**：只有一份 `dynm`。参数是胖指针（数据指针 + 虚表指针）；调用时读虚表的第 k 项再间接跳转。虚表在编译期为每个「类型 × trait」生成一份，里面除方法外还有 `drop` 函数、类型大小和对齐，所以 `Box<dyn Shape>` 能正确释放。
- **Go 接口**：与 `dyn` 同构，接口值是 `(itab 指针, 数据指针)`，调用读 itab 的方法槽。Go 没有单态化式的泛型（用 GC shape 加字典，见泛型实现一节），所以接口调用是最常见的动态分派来源。
- **Java**：类型指针在对象头里，虚表按类存放。

一个关键差别：动态分派的「**选择权**」在哪。Rust 把选择权给调用方（同一个 trait 既能泛型也能 `dyn`）；Java 和 Go 的接口则默认动态，Java 靠 JIT 把它变回静态，Go 靠编译器的内联和去虚化（devirtualization）。

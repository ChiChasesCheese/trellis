---
id: pl-abstraction-operator-overloading-foundation-rust-ops-traits
node: abstraction.operator-overloading
type: qa
step: 3
---
## Q
Rust 里怎样为自定义类型重载 `+`？为什么 `a + b` 会「吃掉」操作数，怎么解决？

## A
Rust 的运算符是 `std::ops` 里的 **trait**：`+` 对应 `Add`，`*` 对应 `Mul`，`a[i]` 对应 `Index`，`*p` 对应 `Deref`。`a + b` 就是 `Add::add(a, b)` 的语法糖。

关键细节：`add(self, rhs)` 的参数是**按值**接收的，对于没有实现 `Copy` 的类型就意味着**所有权被移走**：

```rust
let c = a + b;
println!("{:?}", a);
// error[E0382]: borrow of moved value: `a`
// note: calling this operator moves the left-hand side
```

对 `Vec` 这类要复制才能保留的类型，每次加法都复制太浪费，所以惯例是**同时为引用实现**：

```rust
impl Add for V2  { type Output = V2; fn add(self, o: V2) -> V2 { /* ... */ } }
impl Add for &V2 { type Output = V2; fn add(self, o: &V2) -> V2 { /* ... */ } }
let c = &a + &b;     // 借用，a 和 b 之后仍可用
```

因为运算符是普通 trait，它们能出现在泛型约束里，写出对所有「能相加」的类型都有效的函数：

```rust
fn total<T: Add<Output = T> + Copy>(a: T, b: T) -> T { a + b }
total(1, 2);       // 3
total(1.5, 2.0);   // 3.5
```

这与 Python 不同：Python 的 `+` 在运行期查方法，Rust 的在编译期就解析为具体实现，可以内联，零运行期成本。

---
id: pl-abstraction-encapsulation-foundation-rust-module-privacy
node: abstraction.encapsulation
type: qa
step: 4
---
## Q
Rust 的可见性规则是什么？`pub`、`pub(crate)`、`pub(super)` 分别划定了怎样的边界？

## A
Rust 的默认是**私有**，边界是**模块**（`mod`，可以嵌套）：一个条目（函数、结构体、字段）默认只在定义它的模块内可见，**包括它的子模块**，但父模块和兄弟模块不行。

```rust
mod bank {
    pub struct Account { balance: i64 }        // 字段没有 pub：私有
    impl Account { pub fn new() -> Self { Account { balance: 100 } } }
    pub mod audit {
        pub fn peek(a: &super::Account) -> i64 { a.balance }  // 子模块能读
    }
}
fn main() {
    let a = bank::Account::new();
    a.balance;
    // error[E0616]: field `balance` of struct `Account` is private
}
```

可见性修饰符的刻度：

- `pub`：对任何能访问到该模块的代码可见（最宽）；
- `pub(crate)`：在整个 crate（包）内可见，对外部使用者不可见，是内部共享的首选；
- `pub(super)`：只对父模块可见；
- `pub(in path)`：指定路径。

结构体的**字段**可见性独立设置：类型可以是 `pub` 而字段是私有，外部只能通过 `new` 之类的函数构造，这样构造函数可以强制检查不变量。

与 Java、Go 相比，Rust 强调**精细可控**：开发者可以精确说出「谁能看到」。它同时没有反射，没有运行期绕开的办法（只有 `unsafe` 里的内存操作，且需要显式标记），所以私有字段是真正的安全边界。

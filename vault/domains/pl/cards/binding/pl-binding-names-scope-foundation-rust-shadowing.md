---
id: pl-binding-names-scope-foundation-rust-shadowing
node: binding.names-scope
type: qa
step: 4
---
## Q
Rust 为什么把遮蔽（shadowing）当作鼓励使用的特性？`let x = x ...` 重新绑定和 `let mut x` 再赋值有什么本质区别？

## A
Rust 里 `let` 每次都声明一个**新变量**，同名时新变量盖住旧的，直到当前块结束。它和 `mut` 的区别：

- `let mut x` 再 `x = ...`：同一个变量，同一个类型，原地改值。
- `let x = f(x)`：一个新变量，可以换类型，之后旧值不可再访问。

```rust
let input = "42";                       // &str
let input: i32 = input.parse().unwrap(); // i32, old input is gone
let input = input * 2;
println!("{input}");                    // 84
let x = 5;
{ let x = x * 2; println!("inner {x}"); } // inner 10
println!("outer {x}");                    // outer 5
```

典型用法是数据**变形**：字符串变数字、`Option` 解包、可变变为不可变（`let data = data;` 冻结）。好处是每一步都不用想新名字（`input_str`、`input_num`），且旧的、类型不对的值被彻底遮蔽，无法误用。

内层块里的遮蔽出了块就恢复，上面的 `outer 5` 就是这个效果；块本身也是表达式，最后一个不带分号的表达式是它的值：`let v = { let a = 3; a + 1 };` 得到 `4`。

Rust 敢这样做，是因为类型系统和所有权会兜底：遮蔽只改名字绑定，不改数据；旧值若有 `Drop`，仍在作用域结束时才销毁，不会因为被遮蔽而提前释放。

要记住的事实：在 Rust 里「不可变变量 + 遮蔽」是默认的数据流风格，`mut` 是需要时才用的例外。

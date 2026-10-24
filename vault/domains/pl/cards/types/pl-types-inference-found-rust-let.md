---
id: pl-types-inference-found-rust-let
node: types.inference
type: qa
step: 4
---
## Q
Rust 的 `let` 怎样声明变量？什么时候需要写类型标注，什么时候需要 turbofish `::<>`？

## A
`let` 声明变量，默认不可变，要修改需写 `let mut`。类型通常不用写，编译器会从初始值和后续用法推导；需要时写成 `let c: u8 = 7`。数值字面量在没有其他约束时，整数默认是 `i32`，浮点默认是 `f64`。

```rust
let a = 42;                  // i32（默认）
let b = 2.5;                 // f64（默认）
let c: u8 = 7;               // 显式标注
let d = c + 1;               // u8，由 c 推出
println!("{} {} {} {}", a, b, c, d);
let n = "5".parse::<i32>().unwrap();   // turbofish 指定目标类型
println!("{}", n);
```

实际输出 `42 2.5 7 8`，然后 `5`。

turbofish 是 `::<类型>` 的写法，用来在没有其他线索时手动指定泛型函数的类型参数。`"5".parse()` 本身可以解析成任何实现了 `FromStr` 的类型，编译器需要知道目标：要么左边有标注 `let n: i32 = ...`，要么写 `parse::<i32>()`。线索不足时报 `type annotations needed`。

另一个常见例子是 `collect()`：把迭代器的元素收集进某种容器，收集成 `Vec` 还是 `String`，同样由左边的标注决定。

规则：函数签名、结构体字段必须写类型，函数体内部的局部变量可以省略。这条边界与 Go、Java 一致。

---
id: pl-functional-generators-foundation-rust-gen-async
node: functional.generators
type: qa
step: 5
---
## Q
Rust 的 `gen` 块是什么状态？`async fn` 与生成器在编译器里是什么关系？

## A
Rust 稳定版（1.99）里**没有**可用的 `yield` 或 `gen` 块：

```rust
let g = gen { yield 1; yield 2; };
// error[E0658]: gen blocks are experimental
```

在 2024 edition 里 `gen` 已经被保留为关键字，但特性仍在实验阶段。想要惰性序列时，用 `Iterator` 手写，或者用迭代器适配器链。

但协程的机制在 Rust 里早就存在，就是 `async fn`。编译器把 `async fn` 变成一个**状态机**：每个 `.await` 是一个暂停点，所有跨暂停点存活的局部变量保存成一个枚举里的字段。它是无栈协程，大小在编译期已知：

```rust
async fn two_steps(x: u64) -> u64 {
    let a = [0u8; 100];
    tick().await;              // 暂停点：a 要跨过它存活
    a.len() as u64 + x
}
size_of_val(&two_steps(1))     // 120
```

实测这个 future 占 120 字节，大致是那 100 字节数组加上参数和状态标记。没有 `await` 就没有暂停点，不需要存数组。future 在被 `.await` 或被执行器轮询之前什么都不做，这与 Python 里调用生成器函数不执行函数体一脉相承。

所以三门语言的关系是：Python 的生成器是语言内置的无栈协程；Rust 的 `async` 是同一个机制，只是用来表达「等待」而不是「产出」，生成器版本还没稳定；Go 的 goroutine 是有栈协程。理解这个共同模型，就能明白为什么 `async` 有「着色」问题（暂停点必须出现在 `async` 函数本身，不能藏在普通函数里）。

---
id: pl-abstraction-generics-foundation-rust-generics
node: abstraction.generics
type: qa
step: 4
---
## Q
Rust 的泛型怎么写？trait 约束和 `where` 子句是什么，函数体里能对 `T` 做什么、不能做什么？

## A
Rust 用尖括号声明类型参数，用 **trait 约束**（trait bound）要求它实现某些 trait。trait 是一份能力清单，约束就是「`T` 必须具备这些能力」。

```rust
fn largest<T: PartialOrd>(xs: &[T]) -> &T {
    let mut m = &xs[0];
    for x in xs { if x > m { m = x } }
    m
}
largest(&[3, 9, 2]);   // 9
largest(&[P, P]);      // P 没有实现 PartialOrd
// error[E0277]: can't compare `P` with `P`
```

约束多了可读性差，可以改写成 `where` 子句，把约束放到函数签名后面：`fn f<T, U>(..) where T: A + B, U: C`。

关键规则：**函数体只能使用约束保证存在的操作**。不加约束就写比较：

```rust
fn bigger<T>(a: T, b: T) -> bool { a > b }
// error[E0369]: binary operation `>` cannot be applied to type `T`
// help: consider restricting type parameter `T` with trait `PartialOrd`
```

泛型函数在**定义处**就被完整检查（只对照约束），不是在每次使用时检查。这使得错误信息出现在函数定义处，并且告诉你该加什么约束。这一点与 C++ 模板（在实例化时才检查）形成对比，是现代泛型的共同设计。

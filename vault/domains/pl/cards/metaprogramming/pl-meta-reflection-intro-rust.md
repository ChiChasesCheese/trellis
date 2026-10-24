---
id: pl-meta-reflection-intro-rust
node: metaprogramming.reflection
type: qa
step: 5
---
## Q
Rust 没有运行时反射，那 `Any` 和 `TypeId` 是什么？当需要「面对不认识的类型」时，Rust 怎样替代反射？

## A
**事实**：Rust 编译后，结构体的字段名、方法名、类型名几乎都被擦除，只剩机器码和偏移量。运行时无法问「这个值有哪些字段」。唯一保留的是每个类型一个唯一的编号 `TypeId`，以及基于它的标准库 trait `Any`。

**`Any` 能做什么**：让你把任意值放进 `&dyn Any`（一个可存放任何类型的引用），再问「它是不是我期望的那个类型」，是就取回来（向下转换，downcast）。它只能回答「是或不是」，不能枚举结构。

```rust
fn describe(x: &dyn Any) -> String {
    if let Some(i) = x.downcast_ref::<i32>() { format!("i32 {i}") }
    else if let Some(s) = x.downcast_ref::<String>() { format!("String {s}") }
    else { "unknown".into() }
}
```

传入 `5i32` 得到 `i32 5`，传入 `String` 得到 `String a`，传入自定义结构体得到 `unknown`。`std::any::type_name::<Vec<Option<u8>>>()` 能得到字符串 `alloc::vec::Vec<core::option::Option<u8>>`，主要用于调试。

**真正的替代方案**是把「需要面对不认识的类型」改成「在编译期为每个具体类型生成一份代码」：类型实现一个 trait（比如 serde 的 `Serialize`），这个实现由 `#[derive(Serialize)]` 在编译期按字段展开。运行时面对的是普通的 trait 调用，没有任何查表。

**要记住的一点**：Rust 不是不能做 JSON 序列化，而是把「读字段」这件事在编译时做完了。

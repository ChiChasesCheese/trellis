---
id: pl-errors-result-type-mechanism
node: errors.result-type
type: qa
step: 5
---
## Q
`Result<T, E>` 在内存里是什么样？`?` 运算符展开成什么，错误类型转换发生在哪里？

## A
`Result<T, E>` 是一个枚举（带标签的联合体）：一个标签（成功还是失败）加上一块足够放下较大变体的空间。`Option<T>` 同理。编译器还会做**空位优化**（niche optimization）：如果 `T` 有永远不会出现的取值（引用和 `Box` 不会是 0），就用那个取值表示 `None`，不再单独存标签。所以 `Option<Box<i32>>` 与 `Box<i32>` 一样是 8 字节，空值检查的成本等同于 C 里的空指针检查，却是类型安全的。

`?` 是语法糖。表达式 `x?` 大致展开为：

```rust
match x {
    Ok(v) => v,
    Err(e) => return Err(From::from(e)),
}
```

两个细节：
1. **早返回**：失败时当前函数立刻返回，成功时表达式的值就是 `v`，所以一连串可能失败的步骤可以写成直线代码。
2. **`From::from(e)` 做错误类型转换**：被调用函数的错误类型（比如 `ParseIntError`）如果实现了 `From<ParseIntError> for MyError`，`?` 会自动把它转换成当前函数声明的错误类型。这样不同来源的错误能汇聚到一个统一的错误类型上，无需手写转换。

`?` 也适用于 `Option`，但不能混用：在返回 `Option` 的函数里对 `Result` 用 `?` 是编译错误，编译器提示可以用 `.ok()?` 显式丢弃错误信息。

成本：成功路径没有分配，也没有栈展开；失败路径同样只是一次返回。栈追踪不会自动产生（`anyhow` 等库在需要时才捕获 backtrace）。

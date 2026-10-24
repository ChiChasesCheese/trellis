---
id: pl-types-type-conversions-unique-rust-tiers
node: types.type-conversions
type: qa
step: 7
---
## Q
Rust 为什么把转换分成 `as`、`From` 和 `TryFrom` 三档？这说明它怎样看待「失败」？

## A
Rust 的立场是：转换会不会失败，应该写在类型上，而不是留在文档里。于是有三档：

- `From` / `Into`：保证不会失败、不丢信息。`i64::from(5i32)` 总是成功，编译器只允许你为真正无损的转换实现它。
- `TryFrom` / `TryInto`：可能失败，返回 `Result`，调用者必须处理。
- `as`：低层的、有损的转换，截断或饱和，不报错，保留给你明确要这种语义的场景。

```rust
300i32 as u8;                 // 44，静默截断
u8::try_from(300i32);         // Err(TryFromIntError(PosOverflow))
u8::try_from(200i32);         // Ok(200)
"abc".parse::<i32>();         // Err(ParseIntError { kind: InvalidDigit })
```

实际输出：`44`、`Err(TryFromIntError(PosOverflow))`、`Ok(200)`、`Err(ParseIntError { kind: InvalidDigit })`。

三档的存在说明 Rust 的哲学：把「是否可能出错」当作接口的一部分。读到 `.into()` 就知道安全，读到 `.try_into()?` 就知道这里需要处理失败，读到 `as` 就知道有人在做有意的位级操作。`?` 运算符还会顺便用 `From` 把不同的错误类型自动转成调用者的错误类型。

对比：Python 的 `int("abc")` 和 Java 的 `parseInt("abc")` 都抛异常，调用点看不出会失败；Go 的 `strconv.Atoi` 返回 `error`，较接近 Rust，但 `int32(x)` 的缩窄没有任何标记。Rust 付出的是啰嗦，换来每个转换点的风险一眼可见。

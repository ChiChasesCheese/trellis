---
id: pl-types-strong-weak-found-rust-explicit-conversion
node: types.strong-weak
type: qa
step: 3
---
## Q
Rust 里 `as`、`From` / `Into` 和 `TryFrom` 三种转换各是什么？为什么要区分？

## A
Rust 没有隐式数值转换，每次类型变化都要写出来，并且按风险分成三档：

- `From` / `Into`：无损、不会失败的转换。标准库只为真正无损的情形实现它，如 `i64::from(7i32)`。
- `TryFrom` / `TryInto`：可能失败的转换，返回 `Result`，调用者必须处理。
- `as`：低层的数值转换，不检查，可能截断或饱和，始终成功。

```rust
let a: i32 = 7;
let wide = i64::from(a);              // 无损
let narrow = u8::try_from(300i32);    // 装不下，返回 Err
let cast = 300i32 as u8;              // 只留低 8 位
println!("{} {:?} {}", wide, narrow, cast);
```

实际输出：`7 Err(TryFromIntError(PosOverflow)) 44`。`Result` 是一个有两个变体的类型：成功 `Ok(值)` 或失败 `Err(原因)`。

设计意图：转换会不会丢信息，写在方法的名字和类型上。读到 `.into()`，知道这里安全；读到 `try_from`，知道失败要处理；读到 `as`，知道有人在做有意的、可能有损的转换。代价是写法比 Java 的自动加宽啰嗦。

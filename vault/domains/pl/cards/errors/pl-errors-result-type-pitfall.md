---
id: pl-errors-result-type-pitfall
node: errors.result-type
type: qa
step: 6
---
## Q
Rust 的 `?` 和 `main` 返回 `Result` 有什么容易踩的坑？

## A
**坑一：`?` 不能在返回类型不匹配的函数里使用。**

```rust
fn f() -> Option<i32> { let x: i32 = "5".parse::<i32>()?; Some(x) }
```

```console
error[E0277]: the `?` operator can only be used on `Option`s, not `Result`s,
in a function that returns `Option`
  use `.ok()?` if you want to discard the `Result<Infallible, ParseIntError>` error information
```

`Option` 与 `Result` 不能混用，错误类型也要能通过 `From` 转换到函数返回的错误类型，否则编译失败。这个提示里的 `.ok()?` 意味着主动丢弃了错误原因，要想清楚是否合适。

**坑二：错误信息丢失与 `Box<dyn Error>` 的代价。**

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let n: i32 = "x".parse()?;
    Ok(())
}
```

实测运行：

```console
Error: ParseIntError { kind: InvalidDigit }
```

进程退出码是 1。`main` 返回 `Err` 时，输出的是错误的 `Debug` 形式，对最终用户不友好，也没有上下文说明「是解析哪个值失败」。应用层应当在 `?` 之前加 `.context(...)`，或在 `main` 里自己格式化错误并选择退出码。

用 `Box<dyn Error>` 擦除了具体类型，之后调用者只能通过 `downcast_ref` 恢复，容易失败。

**坑三：习惯性 `unwrap`**，把本该由类型保证的安全变回运行时 panic。

**坑四：错误类型膨胀**。每个函数一个错误枚举，或把所有变体放进一个巨大的枚举，都难以维护。经验：按模块或按调用者需要的区分来划分错误类型。

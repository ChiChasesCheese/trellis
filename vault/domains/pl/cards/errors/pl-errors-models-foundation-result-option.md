---
id: pl-errors-models-foundation-result-option
node: errors.models
type: qa
step: 4
---
## Q
Rust 的 `Option` 和 `Result` 是什么？为什么说它们让编译器强制你处理失败？

## A
Rust 用两个内置的枚举（enum，一个值只能是若干“变体”中的一种）表示“可能没有”和“可能失败”：
- `Option<T>`：要么是 `Some(值)`，要么是 `None`。用来代替“空指针”。
- `Result<T, E>`：要么是 `Ok(成功值)`，要么是 `Err(错误)`。

要拿到里面的值，必须先用 `match` 说明两种情况各怎么办，编译器检查你没漏掉任何变体：

```rust
match "12x".parse::<i32>() {
    Ok(n)  => println!("{}", n),
    Err(e) => println!("bad: {}", e),     // bad: invalid digit found in string
}
```

如果调用了返回 `Result` 的函数却不处理结果，编译器给出警告：`unused Result that must be used`。想主动忽略必须写 `let _ = ...`，留下可见的痕迹。

`v.get(5)` 对越界下标返回 `None` 而不是崩溃；`.unwrap_or(0)` 表示“没有就用 0”。

另外，后缀运算符 `?`：写在一个 `Result` 后面，表示“成功就取出值继续，失败就让当前函数立刻返回这个错误”，是处理链式调用的简写。

要记住的一个事实：成功与失败在**返回类型**里；类型系统让你不处理失败就拿不到值。

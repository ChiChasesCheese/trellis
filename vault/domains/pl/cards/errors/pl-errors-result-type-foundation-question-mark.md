---
id: pl-errors-result-type-foundation-question-mark
node: errors.result-type
type: qa
step: 3
---
## Q
Rust 的 `?` 运算符是什么？它怎么让一串可能失败的步骤写成直线代码？

## A
如果每一步都 `match` 一次 `Result`，代码会被样板淹没。`?` 是一个后缀运算符：对一个 `Result` 写 `x?`，意思是“成功就取出里面的值继续；失败就立刻让**当前函数**返回这个错误”。

```rust
fn port(cfg: &[(&str, &str)]) -> Result<u16, ConfigError> {
    let raw = cfg.iter().find(|(k, _)| *k == "port")
        .map(|(_, v)| *v)
        .ok_or_else(|| ConfigError::Missing("port".into()))?;   // missing -> return Err
    let p: u16 = raw.parse()?;                                  // bad number -> return Err
    Ok(p)
}
```

调用结果（本机实测）：`port(&[("port","8080")])` 得到 `Ok(8080)`；缺键得到 `Err(Missing("port"))`；值非法则返回 `BadNumber` 变体，打印为 `bad number: invalid digit found in string`。

第二处 `?` 作用在 `ParseIntError` 上，函数却声明返回 `ConfigError`：`?` 会自动调用 `From`（“如何从一种类型转成另一种类型”的约定），只要你为 `ConfigError` 写过 `From<ParseIntError>`，就能转换。函数返回类型必须是 `Result`（或 `Option`）才能用 `?`；在 `main` 里用就把 `main` 声明成返回 `Result`。

要记住的一个事实：`?` 只是早返回加类型转换的语法糖，失败仍然是显式返回值，只是样板由编译器生成。

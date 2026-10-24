---
id: pl-errors-result-type-foundation-option-result
node: errors.result-type
type: qa
step: 2
---
## Q
`Result<T, E>` 和 `Option<T>` 的值长什么样？怎样创建、检查和转换它们？

## A
它们是枚举（enum）：一个值在若干“变体”中只能是一个，变体可以携带数据。

```rust
enum Option<T> { Some(T), None }
enum Result<T, E> { Ok(T), Err(E) }
```

创建与检查：

```rust
let a: Option<&i32> = v.get(5);        // None: index out of range
let b: Option<&i32> = v.get(1);        // Some(&20)
let n: Result<i32, _> = "12x".parse::<i32>();   // Err(ParseIntError { kind: InvalidDigit })
```

处理方式：
- `match` 逐个变体处理；
- `unwrap_or(0)`：`None`/`Err` 时给默认值；
- `ok_or(错误)`：把 `Option` 转成 `Result`；
- `map_err(f)`：转换错误的类型；
- `collect::<Result<Vec<_>, _>>()`：把一串 `Result` 汇成一个，遇到第一个 `Err` 就停（对 `["3","x","5"]` 得到 `Err(...)`）；
- `unwrap()` / `expect("msg")`：取值，遇到 `None`/`Err` 就 panic。

要记住的一个事实：成功和失败是同一个类型的两个变体，互斥；不处理另一个变体就拿不到值。

---
id: pl-types-type-conversions-found-parse
node: types.type-conversions
type: qa
step: 4
---
## Q
把字符串解析成数字时，Python、Java、Rust、Go 各自怎样表示失败？

## A
解析（parse）是最容易失败的转换，因为输入来自外部。四门语言用了三种失败信号：

- Python：`int("12x")` 抛出 `ValueError: invalid literal for int() with base 10: '12x'`。
- Java：`Integer.parseInt("12x")` 抛出 `NumberFormatException`，消息是 `For input string: "12x"`。
- Rust：`"12x".parse::<i32>()` 返回 `Result`，失败时是 `Err(ParseIntError { kind: InvalidDigit })`，不抛异常。
- Go：`strconv.Atoi("12x")` 返回两个值 `(0, err)`，`err` 是错误值。

```rust
let ok = "12".parse::<i32>();
let bad = "12x".parse::<i32>();
println!("{:?} {:?}", ok, bad);
match bad { Ok(n) => println!("{}", n), Err(e) => println!("error: {}", e) }
```

实际输出：`Ok(12) Err(ParseIntError { kind: InvalidDigit })`，然后 `error: invalid digit found in string`。

区别在于失败是否出现在函数签名里。Rust 和 Go 把失败放进返回值，调用者看到类型就知道要处理；Java 和 Python 的异常在签名里不可见（Java 的 `NumberFormatException` 是非受检异常），忘了 `try/except` 也能编译或运行，直到遇到坏输入才崩溃。

另有一个常见的陷阱：Python 的 `int(3.9)` 是 3（向零截断），`int("3.9")` 却抛 `ValueError`；`bool("0")` 是 `True`，因为非空字符串都是真。

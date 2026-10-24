---
nodes: [errors.models, errors.error-values, errors.exceptions, errors.result-type, memory.resource-management]
tags: [drill]
---
# 练习：错误悄悄消失的四种方式

四个服务各用一门语言，线上都出现过同一种症状：请求明明失败了，却返回成功，日志里也没有原因。事后复盘发现，每个服务都踩了自己语言错误处理模型里的一个经典坑。你要预测下面片段的输出，把症状对应到机制，并为每门语言写出一条能在评审里拦住它的规则。

```go
type MyErr struct{}
func (*MyErr) Error() string { return "my error" }
func mayFail(fail bool) error {
    var e *MyErr
    if fail { e = &MyErr{} }
    return e
}
err := mayFail(false)
fmt.Println(err == nil, err != nil); fmt.Printf("%T\n", err)
```

```java
static int f() { try { throw new RuntimeException("boom"); } finally { return 1; } }
// 另一处：try (var r = 资源) { throw new Exception("body failed"); }，而 r.close() 抛出 Exception("close failed")
```

```python
def f():
    try:    raise RuntimeError("boom")
    finally: return 1
print(f())
```

```rust
let n: i64 = s.trim().parse()?;   // 函数返回 Result<i64, AppError>，AppError 实现了 From<ParseIntError>
```

**要你给出的**
- Go 片段的输出，以及 `mayFail(false)` 之后调用者的 `if err != nil` 会走哪条分支；Java 与 Python 的 `f()` 返回什么。
- Java 的 try-with-resources 里，调用者最终收到哪个异常，另一个去了哪里。
- Rust 的 `?` 在解析失败时具体做了哪两件事。
- 每门语言一条评审规则，外加一条跨语言的「错误值必须被谁看见」原则。

**评分要点**
- Go 输出 `false true` 和 `*main.MyErr`：接口值由（类型，值）两部分组成，装进一个值为 `nil` 的 `*MyErr` 后，类型部分不是空，整个 `error` 就不等于 `nil`。调用者会走错误分支，把「没出错」当作出错。规则：返回 `error` 的函数里不要声明具体的错误指针变量，直接 `return nil` ([[pl-errors-error-values-pitfall-typed-nil]], [[pl-sig-go-pitfall-nil-interface]])。
- Go 的包装用 `fmt.Errorf("...: %w", err)`，判断用 `errors.Is` / `errors.As`：`errors.Is(e, ErrNotFound)` 为 `true`，而 `e == ErrNotFound` 为 `false`，信息是 `user 42: not found`。直接用 `==` 比较会漏掉所有被包装过的错误 ([[pl-errors-error-values-foundation-wrapping]], [[pl-errors-error-values-foundation-sentinel-custom]])。
- Java 的 `f()` 返回 `1`，异常被 `finally` 里的 `return` 吞掉；Python 同样返回 `1`，并且 Python 3.14 会对 `finally` 里的 `return` 给出 `SyntaxWarning`。规则：`finally` 里不写 `return`、不抛异常，只做清理 ([[pl-errors-exceptions-pitfall-finally]], [[pl-errors-exceptions-foundation-finally-chain]])。
- try-with-resources：调用者收到 `body failed`，`close failed` 被记录为被抑制异常（suppressed），用 `getSuppressed()` 才看得到；Python 的对应机制是异常链 `__context__`，在 `except` 里再抛新异常时，旧异常挂在 `__context__` 上 ([[pl-memory-resource-management-foundation-java]], [[pl-errors-exceptions-mechanism]])。
- Rust 的 `?` 做两件事：失败时通过 `From<ParseIntError>` 把底层错误转换成 `AppError`，然后立即从当前函数返回 `Err`。三个输入 `"42"`、`"-7"`、`"x1"` 的输出是 `ok 42`、`err negative: -7`、`err parse: invalid digit found in string`。错误是返回类型的一部分，忽略它要显式写 `let _ =` ([[pl-errors-result-type-foundation-question-mark]], [[pl-errors-result-type-foundation-thiserror-anyhow]])。
- 四种模型的共同弱点不同：Go 和 Rust 的错误是值，可能被忽略或写错分支；Java 和 Python 的异常自动向上传播，可能被中途吞掉。选择模型就是选择在哪里最容易丢错 ([[pl-errors-models-table]], [[pl-errors-models-pitfall-ignored]])。
- 跨语言原则：每个错误要么被处理，要么带着上下文向上传递，不允许两者都没有；用静态检查工具和代码评审清单把「吞错」变成可发现的缺陷 ([[pl-errors-models-best-practice]], [[pl-errors-result-type-pitfall]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：

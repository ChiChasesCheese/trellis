---
id: pl-errors-error-values-mechanism
node: errors.error-values
type: qa
step: 2
---
## Q
Go 的错误包装（`%w`）、`errors.Is` 和 `errors.As` 在底层是怎么工作的？

## A
`error` 是接口，运行时表示为两个指针：动态类型和指向数据的指针。包装错误（wrap）就是创建一个新的错误值，其中保存了被包装的那个错误：

```go
fmt.Errorf("find %d: %w", id, ErrNotFound)
```

`%w` 让返回的值实现了 `Unwrap() error` 方法，返回被包装的错误。自定义类型也可以自己实现 `Unwrap`。逐层包装之后就形成一条**错误链**：

```console
run: parse config: open /nope: no such file or directory
```

这一行是三层各自加了一段上下文后拼起来的结果：最外层 `run`，中间 `parse config`，底层是标准库的 `*fs.PathError`。

- **`errors.Is(err, target)`**：沿着链逐层 `Unwrap`，在每一层检查「是否等于 `target`」（用 `==`，或错误类型自己的 `Is` 方法）。用于判断「是不是这个已知的错误」，例如 `errors.Is(err, fs.ErrNotExist)`。
- **`errors.As(err, &target)`**：沿着链找到第一个可以赋值给 `target` 类型的错误，并取出它，用于访问错误里携带的字段，例如从链中取出 `*fs.PathError` 读它的 `Path`。
- **`errors.Join(a, b)`**（Go 1.20）：把多个错误合成一个，`Unwrap() []error` 返回全部，`Is`/`As` 会检查所有分支。

判断错误种类的两种方式对应两种设计：**哨兵错误**（sentinel error，包级变量，如 `io.EOF`）表示一个具体状态；**错误类型**（自定义 struct）携带结构化信息。

成本：`fmt.Errorf` 要格式化字符串并分配，本机测量约 37 ns 每次，不在高频路径上使用。

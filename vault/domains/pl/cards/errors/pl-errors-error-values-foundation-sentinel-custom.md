---
id: pl-errors-error-values-foundation-sentinel-custom
node: errors.error-values
type: qa
step: 2
---
## Q
Go 里哨兵错误（sentinel error）和自定义错误类型是什么？各在什么时候用？

## A
`error` 接口只要求一个方法 `Error() string`，所以有两种常见的造错误的方式：

**哨兵错误**：包级别的一个预先创建的错误变量，用来表示一个具体、固定的状态：

```go
var ErrNotFound = errors.New("not found")        // one value, compared by identity
```

标准库里有 `io.EOF`、`fs.ErrNotExist`。调用者用 `err == ErrNotFound`（或后面的 `errors.Is`）判断“是不是这个状态”。

**自定义错误类型**：自己定义一个结构体并实现 `Error()`，可以携带结构化信息：

```go
type ValidationError struct{ Field string; Err error }
func (e *ValidationError) Error() string { return "invalid " + e.Field + ": " + e.Err.Error() }
```

调用者通过类型断言或 `errors.As` 取出它，读 `Field` 之类的字段，据此决定如何处理。

选择：只需要判断“是不是这种情况”用哨兵；需要带上下文数据（哪个字段、哪个 id、状态码）用自定义类型。两者一旦被导出，就成了包的 API 的一部分，调用者会依赖它们，不能随便改。

要记住的一个事实：Go 里区分错误种类靠的是普通的值和类型，不是专门的语言机制。

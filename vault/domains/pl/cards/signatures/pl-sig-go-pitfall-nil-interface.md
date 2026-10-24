---
id: pl-sig-go-pitfall-nil-interface
node: signatures.go
type: qa
step: 9
---
## Q
Go 里“值为 nil 的接口不等于 nil”是怎么回事？这个陷阱怎样在返回 `error` 的函数里出现，修复方法是什么？

## A
**机制**：接口值在内存里是一对（类型，值）。只有当**两者都为空**时，接口才等于 `nil`。如果你把一个值为 `nil` 的**具体类型指针**赋给接口，接口里就有了类型信息，接口本身不再是 `nil`。

```go
type MyErr struct{}
func (*MyErr) Error() string { return "my error" }

func mayFail(fail bool) error {
    var e *MyErr
    if fail { e = &MyErr{} }
    return e                    // returns a non-nil error interface!
}
err := mayFail(false)
fmt.Println(err == nil)         // false
```

真实输出：`err == nil` 是 `false`，`err != nil` 是 `true`。再看单独的例子：`var p *MyErr; var i error = p` 的输出是 `p == nil` 为 `true`，`i` 的类型是 `*main.MyErr`，`i == nil` 为 `false`。

**生产后果**：函数“没有出错”，调用方的 `if err != nil` 却进入了错误分支，随后调用 `err.Error()` 可能在 nil 接收者上出错或打印出莫名其妙的错误。症状：偶发的“明明成功却报错”。

**修复**：函数在无错误时**直接返回字面量 `nil`**，永远不要返回一个可能是 nil 的具体类型变量作为接口：

```go
if fail { return &MyErr{} }
return nil
```

**更一般的规则**：返回 `error` 的函数，其内部变量类型就用 `error`，不要用具体的错误类型指针。

**同类的 Go 陷阱**：`for` 循环变量在 Go 1.22 之前被所有闭包共享（现在每次迭代独立）；对 `append` 得到的切片别名；对 `nil` map 写入会 panic；`defer` 在循环里累积到函数返回才执行。`go vet` 和 `staticcheck` 能抓住其中一部分。

**教训**：Go 的“简单”是表面的简单，接口的内部表示是你必须了解的一块真实复杂度。

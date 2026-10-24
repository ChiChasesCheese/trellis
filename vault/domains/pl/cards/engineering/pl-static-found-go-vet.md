---
id: pl-static-found-go-vet
node: engineering.static-analysis
type: qa
step: 2
---
## Q
Go 的 `go vet` 和 staticcheck 分别是什么？`go vet` 为什么只做「把握很大」的检查？

## A
**`go vet`** 是 Go 工具链自带的静态检查器，专抓「能编译、但几乎肯定是错的」写法。`go test` 运行时还会自动跑其中一小部分最可靠的检查。

**例**：

```go
type Counter struct {
    mu sync.Mutex
    n  int
}

func (c Counter) Inc() { c.mu.Lock(); c.n++; c.mu.Unlock() } // value receiver

func Show(id int) { fmt.Printf("id=%s\n", id) }
```

`go build` 顺利通过，`go vet` 报告：

```text
a.go:13:9: Inc passes lock by value: sa.Counter contains sync.Mutex
a.go:15:36: fmt.Printf format %s has arg id of wrong type int
```

第一条是真正的逻辑错误：值接收者会复制整个 `Counter`，包括锁，每次调用锁住的是副本，`n++` 也只改了副本，什么同步都没做到。第二条是格式化动词与参数类型不匹配，运行时只会打印出 `%!s(int=7)` 这样的乱码。

**为什么 `go vet` 保守**：Go 的原则是只收「误报极少」的检查，因为 `go vet` 会被默认在测试里运行，一旦误报多，开发者就会学会忽略它。更激进的规则不放进官方工具，交给社区。

**staticcheck**（第三方）做更深的检查：已弃用的 API、永远为真的条件、没用的赋值、可简化的代码。`golangci-lint` 是把几十个 linter 聚合起来的运行器，团队常用它统一配置和 CI 入口。

**Go 的另一个选择**：「未使用的变量」和「未使用的导入」在 Go 里是**编译错误**，而不是警告。这体现 Go 的取舍：宁可让编译器强硬，也不要一堆被忽略的警告。

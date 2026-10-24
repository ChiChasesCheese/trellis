---
id: pl-eco-tooling-pitfall-unchecked-build
node: ecosystem.tooling
type: qa
step: 10
---
## Q
“编译通过”不等于“检查通过”。Go 里 Printf 格式错误能编译、能运行、`go test` 又会失败，这个落差在生产中怎样出事？

## A
`go build` 和 `go run` **不运行** `go vet`。下面这段有明显的格式串错误，但编译顺利通过：

```go
func Show() { fmt.Printf("%d items\n", "three") }
// go build . && go run .
// %!d(string=three) items
```

真实输出是 `%!d(string=three) items`：没有 panic，没有报错，只是日志里多了一段怪文本。在日志、监控、告警文案里，这类“静默的错误输出”可能很久没人发现。

加一个调用它的测试后，`go test` 会自动运行 vet 的子集，直接失败：

```
./main.go:5:27: fmt.Printf format %d has arg "three" of wrong type string
FAIL	vt [build failed]
```

**含义**：同一份代码，`build` 说没问题，`test` 说有问题，取决于你运行的是哪一个命令。如果 CI 只跑 `go build`（比如只构建镜像）而没有跑 `go test` 或 `go vet`，这个缺陷就会进入生产。

**其他语言的同类落差**：
- **Java**：`javac` 默认不开大部分 lint，`Integer` 用 `==` 比较（超出缓存范围的两个 `1000` 不相等）编译不报警，需要 Error Prone 或 `-Xlint` 之类。
- **Rust**：编译通过，但 `clippy` 能抓出大量惯用法问题与潜在 panic；不在 CI 里运行就等于没有。
- **Python**：解释器对未使用的导入、裸 `except`、可变默认参数全部沉默，只有 `ruff` 会报告（它的 `B006` 抓到 `def add(x, items=[])`，运行时该函数连续调用会得到 `[1, 2] [1, 2]` 这种共享状态结果）。

**防线**：把检查命令写进 CI 的必经步骤（`go vet ./...`、`cargo clippy -- -D warnings`、`ruff check`、`mvn verify`），并确认 CI 的命令和本地一致；出现“本地通过 CI 失败”或相反时，第一件事是核对两边的工具版本与命令。

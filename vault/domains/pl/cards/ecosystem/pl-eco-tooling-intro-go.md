---
id: pl-eco-tooling-intro-go
node: ecosystem.tooling
type: qa
step: 2
---
## Q
Go 自带哪些工具：`gofmt`、`go vet`、`go test`？每个做什么，一个例子里它们的输出是什么？

## A
Go 把基础工具链都放进 `go` 命令和标准发行版，无需额外安装。

**`gofmt`**（也可用 `go fmt`）：把代码重写成唯一的标准格式，几乎没有配置项。缩进用制表符，花括号位置固定，空格规则固定。输入一段排版混乱的代码，`gofmt -d` 显示的差异是：把挤在一行的 `import ("fmt"\n"os")` 展开成多行括号块并缩进，`fmt.Println( x )` 变成 `fmt.Println(x)`，单行 `if true { ... }` 展开为多行。结果与谁在写无关，只要运行过 `gofmt`，格式就完全一致。

**`go vet`**：静态检查常见错误。例如格式串和参数不符：

```go
fmt.Printf("%d items\n", "three")
// go vet: fmt.Printf format %d has arg "three" of wrong type string
```

它检查 Printf 家族、结构体 tag 格式、不可达代码、复制锁等。

**`go test`**：测试运行器。约定：`_test.go` 文件里以 `Test` 开头的函数就是测试，`go test ./...` 运行全部；还有基准（`Benchmark`）、模糊测试（`Fuzz`）、覆盖率（`-cover`）、竞争检测（`-race`），全部内置。**`go test` 会自动运行 `go vet` 的一个子集**，其中包括 Printf 检查。

**严格的编译期规则也算工具链的一部分**：未使用的导入和未使用的局部变量是**编译错误**，不是警告。

**要记住的一点**：Go 的立场是“工具链提供一种做法”：所有 Go 项目格式相同、测试方式相同、基准方式相同。

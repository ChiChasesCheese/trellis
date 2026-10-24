---
id: pl-testing-found-go-table
node: engineering.testing
type: qa
step: 2
---
## Q
Go 的表驱动测试（table-driven test）是什么？Go 为什么不提供断言函数，反而形成了这种写法？

## A
Go 的测试就是普通函数 `func TestXxx(t *testing.T)`，放在 `_test.go` 文件里，由 `go test` 运行。标准库没有 `assertEqual` 之类的断言：自己写比较，失败时调用 `t.Errorf`（记录失败并继续）或 `t.Fatalf`（立即停止）。

**表驱动**：把用例写成结构体切片，循环里用 `t.Run(name, ...)` 把每个用例作为子测试运行。

```go
tests := []struct{ name, in, want string }{
    {"plain", "Hello World", "hello-world"},
    {"double space", "a  b", "a-b"},
}
for _, tc := range tests {
    t.Run(tc.name, func(t *testing.T) {
        if got := Slug(tc.in); got != tc.want {
            t.Errorf("Slug(%q) = %q, want %q", tc.in, got, tc.want)
        }
    })
}
```

`go test -v` 的真实输出（节选；`Slug` 对连续两个空格有 bug）：

```text
=== RUN   TestSlug/double_space
    a_test.go:15: Slug("a  b") = "a--b", want "a-b"
--- FAIL: TestSlug (0.00s)
    --- PASS: TestSlug/plain (0.00s)
    --- FAIL: TestSlug/double_space (0.00s)
```

好处：加一个用例只是加一行；失败信息自带用例名和输入；`go test -run 'TestSlug/double'` 可以单跑一个；结构体字段可以随需求扩展（期望的错误、前置状态）。

**为什么没有断言库**：Go 的价值观是「测试就是普通代码」，用语言本身的 `if` 和 `for` 表达，不引入一套 DSL，也不依赖魔法。代价是比较复杂结构时要自己写 `if`，失败信息也要自己组织。Go 1.22 起每次循环迭代都有独立的循环变量，所以在子测试里加 `t.Parallel()` 不会再出现所有子测试共享最后一个用例的老问题。

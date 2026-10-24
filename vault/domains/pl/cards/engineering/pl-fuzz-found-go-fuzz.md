---
id: pl-fuzz-found-go-fuzz
node: engineering.fuzzing
type: qa
step: 3
---
## Q
Go 内置的模糊测试怎么写、怎么运行？发现问题后它留下什么？

## A
Go 1.18 起，标准库的 `testing.F` 提供模糊测试。写法：`FuzzXxx(f *testing.F)` 里用 `f.Add(...)` 添加种子输入，再用 `f.Fuzz(func(t *testing.T, ...) {...})` 定义被测逻辑（参数只能是字符串、字节切片、基本数值等类型）。

两种运行方式：`go test` 只把种子和已保存的失败输入当作普通单元测试跑一遍；`go test -fuzz=FuzzParse -fuzztime=15s` 才进入真正的变异循环。

**例**：解析 `"<长度>:<内容>"`，既没检查长度是否越界，也没处理缺少冒号：

```go
func Parse(s string) string {
    i := 0
    for i < len(s) && s[i] != ':' { i++ }
    n, err := strconv.Atoi(s[:i])
    if err != nil { return "" }
    return s[i+1 : i+1+n]
}
```

种子是 `"3:abc"`，不到一秒就失败了：

```text
--- FAIL: FuzzParse
    panic: runtime error: slice bounds out of range [:2] with length 1
```

同时在 `testdata/fuzz/FuzzParse/` 下写入一个文件，内容是缩小后的最小输入：

```text
go test fuzz v1
string("0")
```

输入 `"0"`：没有冒号，`i` 走到字符串末尾，`s[i+1:]` 越界。

**这个文件的意义**：此后普通的 `go test` 会自动重放它，成为回归测试，应当提交进仓库。修复 bug 后它依然保留，保证同类问题不会再出现。

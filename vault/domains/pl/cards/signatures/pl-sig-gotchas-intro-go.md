---
id: pl-sig-gotchas-intro-go
node: signatures.gotchas
type: qa
step: 2
---
## Q
Go 最值得认识的经典陷阱有哪些：nil 接口、切片别名、nil map、`range` 的副本？每个的真实表现和根源是什么？

## A
**1. 值为 nil 的接口不等于 nil**。接口值是（类型，值）一对，只有两者都空才等于 `nil`。函数返回一个值为 nil 的具体类型指针作为 `error`，调用方的 `err != nil` 成立。真实输出：`mayFail(false) == nil` 为 `false`。根源：接口的内部表示。修法：无错误时直接 `return nil`。

**2. 切片的别名**。子切片与原切片共享底层数组，`append` 是否复制取决于容量：

```go
a := []int{1,2,3,4,5}
b := a[1:3]               // len 2, cap 4
b = append(b, 100)
fmt.Println(a)            // [1 2 3 100 5]
```

真实输出 `[1 2 3 100 5]`：`append` 悄悄改掉了 `a[3]`。根源：切片是（指针、长度、容量）的视图。修法：需要独立副本时 `slices.Clone`，返回子切片时用 `s[a:b:b]` 限制容量。

**3. 写入 nil map 会 panic**。`var m map[string]int` 只声明未初始化，读取得到零值，写入则 `panic: assignment to entry in nil map`（真实输出）。根源：零值设计，map 的零值是 nil。修法：`make(map...)` 或字面量。

**4. `range` 得到的是元素副本**。

```go
for _, t := range ts { t.n *= 10 }     // [{1} {2}], unchanged
for i := range ts { ts[i].n *= 10 }    // [{10} {20}]
```

真实输出：第一个循环不改变切片，第二个才改变。根源：值语义，`t` 是副本。

**5. 循环变量（Go 1.22 前）**：所有闭包共享同一个变量，Go 1.22 起每次迭代独立（按 `go.mod` 版本选择加入）。

**6. `defer` 在循环里累积**，直到函数返回才执行，打开大量文件时可能耗尽文件描述符。

**共同点**：都不会编译失败，要靠 `go vet`、竞争检测器、测试与评审发现。

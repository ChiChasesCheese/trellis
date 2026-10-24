---
id: pl-types-null-safety-found-go-nil-zero
node: types.null-safety
type: qa
step: 4
---
## Q
Go 的 `nil` 和「零值」（zero value）是什么？哪些 `nil` 能直接用，哪些会 panic？

## A
Go 中没有显式初始化的变量会得到零值：数字是 0，布尔是 `false`，字符串是 `""`，而指针、切片（slice）、map、接口、函数的零值是 `nil`。设计目标是让零值本身就有意义、能直接使用，而不是处于未初始化的危险状态。

`nil` 的行为因类型而异：

- `nil` 切片：长度 0，可以直接 `append`。
- `nil` map：可以读（得到零值），不能写。
- `nil` 指针：解引用会 panic（运行时错误导致程序崩溃并打印栈）。

```go
var s []int
s = append(s, 1)
fmt.Println(len(s), s)         // 1 [1]
var m map[string]int
fmt.Println(m["a"], len(m))    // 0 0
var p *U                       // U 是 struct{ Name string }
fmt.Println(p.Name)            // panic
```

实际输出：`1 [1]`、`0 0`，最后一行 `panic: runtime error: invalid memory address or nil pointer dereference`。写 `nil` map（`m["a"] = 1`）则 `panic: assignment to entry in nil map`。

所以 Go 没有消灭空值，只是让大部分情形的 `nil` 无害。判断一个类型的 `nil` 能不能用，要问「这个操作需不需要底层存储已经存在」。标准库的 `sync.Mutex`、`bytes.Buffer` 都设计成零值即可用。

---
id: pl-types-null-safety-unique-go-zero
node: types.null-safety
type: qa
step: 4
---
## Q
Go 的「零值可用」是怎样减少对空值检查的需要的？它和 Rust 的 `Option` 哲学有什么根本区别？

## A
Go 的每个类型都有一个定义好的零值：数值是 0，字符串是空串，布尔是 `false`，切片、map、指针、接口是 `nil`。设计目标是让零值本身就能直接使用，不必先构造：

```go
var s []int
s = append(s, 1)       // 合法
fmt.Println(len(s), s)        // 1 [1]
var m map[string]int
fmt.Println(m["a"], len(m))   // 0 0，读取安全
var p *U
fmt.Println(p.Name)    // panic: nil pointer dereference
```

实际输出：`1 [1]`，`0 0`，最后一行 panic。`sync.Mutex`、`bytes.Buffer` 也都是零值即可用。

写入 `nil` map 则不行：`m["a"] = 1` 会 `panic: assignment to entry in nil map`，因为写入需要分配底层存储，而零值没有。

两种哲学的根本区别在于对「缺失」的态度：

- Rust：缺失是一种需要被类型系统追踪的状态，编译器强制你处理。代价是仪式，收益是线上不会出现空指针。
- Go：尽量让缺失不重要，用有意义的零值替代。收益是代码少、API 简单，代价是 `nil` 的行为分裂：有的 `nil` 无害，有的致命，开发者必须记住哪个类型的 `nil` 能做什么。

Go 并没有消灭空值，只是用惯例和零值把它的危害缩小，所以它仍然会有 nil 指针 panic。

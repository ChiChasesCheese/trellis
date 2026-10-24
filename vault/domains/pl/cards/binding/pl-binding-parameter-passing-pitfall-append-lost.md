---
id: pl-binding-parameter-passing-pitfall-append-lost
node: binding.parameter-passing
type: qa
step: 10
---
## Q
Go 函数里对传入的切片 `append`，为什么调用者有时看到结果、有时看不到？这个行为在生产里会造成什么 bug？

## A
`append` 的结果取决于**容量**：容量够，就写进共享的底层数组；容量不够，就分配一个新数组，把元素搬过去，返回指向新数组的**新切片头**。而函数里的切片头是调用者那份的副本，新头只赋给了函数里的形参。

```go
func add(s []int) { s = append(s, 99) }

a := make([]int, 1, 1)   // len 1, cap 1: full
add(a)
fmt.Println(a)           // [0]    the append is lost

b := make([]int, 1, 4)   // len 1, cap 4: room left
add(b)
fmt.Println(b, b[:2])    // [0] [0 99]
```

第二种情形更危险。`b` 的长度仍是 1，所以打印 `[0]`，但 `99` 其实已经写进了底层数组，用 `b[:2]` 就能读到。同一段代码，仅因为调用者的切片容量不同，行为就不同。

典型 bug：

1. 函数「构造结果」却不返回，容量恰好够时测试通过，数据量变大后偶尔丢数据。
2. 两个切片共享底层数组，一个 `append` 悄悄覆盖了另一个的元素（别名数据损坏）。
3. 把传入的切片存进结构体，调用者之后继续修改它，结构体内容随之改变。

对策：

- 需要增长就返回新切片，签名写成 `func add(s []int, x int) []int`，调用者写 `a = add(a, 1)`。这是 Go 的惯用法，标准库的 `append` 本身就这样设计。
- 需要保存别人的切片时 `slices.Clone` 或 `append([]int(nil), s...)`。
- 需要限制 `append` 的写入范围时，用完整切片表达式 `s[:n:n]` 把容量截到长度，强迫 `append` 分配新数组。

Java 和 Python 没有这种「容量够不够」的分叉：`list.add` 和 `list.append` 永远修改同一个对象。

---
id: pl-memory-value-reference-semantics-foundation-go
node: memory.value-reference-semantics
type: qa
step: 3
---
## Q
Go 里的值、指针和 slice 是怎么回事？赋值和传参时各是复制还是共享？

## A
Go 里变量默认存的就是**值本身**：结构体、数组、整数赋值或传参时整体复制。要共享，就显式取地址得到**指针**（pointer）：`&x` 取变量 `x` 的地址，`*p` 通过指针读写它指向的值。

```go
x := 1
p := &x          // p points to x
*p = 5           // writes x
inc(x)           // func inc(n int) { n++ }  gets a copy
incp(&x)         // func incp(p *int) { *p++ } changes x itself
fmt.Println(x)   // 6
```

`inc(x)` 之后 `x` 仍是 5，`incp(&x)` 之后变成 6。

**slice**（切片）是最容易误解的类型：它本身是一个三字段的小结构体，`(指向数组的指针, 长度 len, 容量 cap)`。赋值 slice 复制的是这三个字段，底层数组被共享：

```go
s := []int{1, 2, 3}
t := s[:2]       // same array, len 2, cap 3
t[0] = 9
fmt.Println(s, len(t), cap(t))   // [9 2 3] 2 3
```

`t` 改了第 0 个元素，`s` 也看到了。map 和 channel 同样是“值里藏着引用”。

要记住的一个事实：Go 默认复制，共享必须写指针；唯独 slice、map 这类自带引用的类型，复制变量也会共享数据。

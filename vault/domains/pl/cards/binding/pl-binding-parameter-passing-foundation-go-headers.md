---
id: pl-binding-parameter-passing-foundation-go-headers
node: binding.parameter-passing
type: qa
step: 4
---
## Q
Go 说「一切都是传值」，为什么往函数里传切片（slice）和 map 却能改到调用者的数据，`append` 却可能没效果？

## A
Go 严格按值传参：每次调用都**复制实参的内容**。区别在于不同类型「内容」是什么：

- 数组 `[3]int`：内容是全部三个元素，整个被复制，函数里改不到调用者。
- 切片：内容是一个 24 字节的**切片头**（指向底层数组的指针、长度、容量）。复制的是头，两个头指向同一个底层数组。
- map、channel：变量本身就是指向运行时内部结构的指针（8 字节），复制指针，共享同一个结构。
- 指针 `*T`：复制地址，共享目标。

```go
func grow(s []int)     { s = append(s, 99) }
func setFirst(s []int) { s[0] = 7 }
func fill(m map[string]int) { m["k"] = 1 }
func bump(a [3]int)    { a[0] = 100 }
// s := make([]int, 1, 1); grow(s)      -> s = [0], len 1
// setFirst(s)                          -> s = [7]
// fill(m)                              -> map[k:1]
// bump(arr)                            -> arr = [1 2 3]
// unsafe.Sizeof: slice 24, map 8, [3]int 24
```

- `setFirst` 改的是底层数组，调用者看得到。
- `grow` 里的 `append` 容量不够，分配了新数组，**新的切片头只赋给形参**，调用者手里的头（长度仍是 1）没变，结果丢失。
- `bump` 改的是数组副本。

规则：想让函数改变切片的**长度**，必须返回新切片（`s = grow(s)`）或传 `*[]int`；只改元素则直接传切片即可。

这是 Go 的刻意设计：没有隐式引用，语义只有一条「复制」，你只需知道每种类型复制的是什么。代价是切片、map 这类「看起来像值、实际带共享」的类型需要记忆。

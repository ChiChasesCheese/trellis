---
nodes: [binding.parameter-passing, binding.evaluation-order]
tags: [drill]
---
# 练习：函数里改了参数，调用者看到什么

一个工具函数 `grow(xs)` 把传入序列的第一个元素改成 99，再追加一个 4。同一个团队的四个服务各用一门语言实现它，评审时有人发现 Go 版本「有时能看到追加的元素，有时看不到」，还有人在赋值语句里写了 `i, arr[i] = 2, 7`，结果在不同语言里写进了不同的位置。你要预测行为、解释原因，并为每门语言写出不会让调用者吃惊的函数约定。

```go
func grow(xs []int) { xs[0] = 99; xs = append(xs, 4) }
a := []int{1, 2, 3}                       // len 3, cap 3
b := make([]int, 3, 10); copy(b, a)       // len 3, cap 10
grow(a); grow(b)
fmt.Println(a, len(a)); fmt.Println(b, len(b), b[:4])

arr := []int{0, 0, 0}; i := 0
i, arr[i] = 2, 7
fmt.Println(i, arr)
```

**要你给出的**
- 上面 Go 代码的三行输出，以及 Python、Java、Rust 里「改第一个元素再追加」各自对调用者可见的结果。
- 同样的赋值意图 `i` 与 `arr[i]` 一起赋值，在 Go、Python、Java（`z[i] = i = 2`）、Rust（`(i, arr[i]) = (2, 7)`）里分别写进哪个下标。
- 每门语言一条「接受并修改序列」的函数约定（签名怎么写、文档怎么写），让调用点看得出会不会被改。

**评分要点**
- Go 三行输出：`[99 2 3] 3`、`[99 2 3] 3 [99 2 3 4]`、`2 [7 0 0]`。切片是（指针、长度、容量）三个字段按值复制：改元素通过同一个底层数组可见，`append` 改的是副本的长度，调用者看不到 ([[pl-binding-parameter-passing-foundation-go-headers]])。
- 容量足够时 `append` 会把 4 写进共享的底层数组，调用者用 `b[:4]` 就能看到；容量不够时则分配新数组，调用者完全不受影响。同一行代码两种结果，取决于调用者的容量 ([[pl-binding-parameter-passing-pitfall-append-lost]])。
- Python 里 `xs[0] = 99` 与 `xs.append(4)` 都改了调用者的列表，而 `xs = xs + [4]` 只是把局部名字绑到新对象，调用者看不到；Java 的 `List`、数组同理，对象引用按值传递，函数里重新赋值不影响外面 ([[pl-binding-parameter-passing-foundation-python-sharing]], [[pl-binding-parameter-passing-foundation-java-value]])。
- Rust 的 `fn grow(mut xs: Vec<i32>)` 会移动所有权，调用后再用 `a` 是编译错误（`borrow of moved value`）；想让调用者看到修改要写 `&mut Vec<i32>`，调用点还必须写 `&mut b`，输出 `[99, 2, 3, 4]` ([[pl-binding-parameter-passing-foundation-rust-move-borrow]], [[pl-binding-parameter-passing-philosophy-explicit-mutation]])。
- 赋值顺序：Go 输出 `2 [7 0 0]`（左边的下标 `i` 先按旧值求出），Python 输出 `2 [0, 0, 7]`（先算右边，再从左到右赋值，赋 `arr[i]` 时 `i` 已经是 2），Rust 的解构赋值同样得到 `2 [0, 0, 7]`，Java 的 `z[i] = i = 2` 得到 `2 [2, 0, 0]`（数组和下标先定）。四门语言没有一个共同答案 ([[pl-binding-evaluation-order-foundation-assignment]], [[pl-binding-evaluation-order-foundation-go]], [[pl-binding-evaluation-order-pitfall-tuple-assign]])。
- 函数约定：Go 要么返回新切片让调用者 `a = grow(a)`，要么文档写明「会修改元素、不会改变长度」；Python 和 Java 在文档里写明是否原地修改，或者直接返回新对象；Rust 让签名说话（`&mut`、返回 `Vec`）。通用做法是修改与返回二选一，不要同时做 ([[pl-binding-parameter-passing-best-practice]], [[pl-binding-parameter-passing-table]])。
- 赋值语句里目标与值有相互依赖的副作用时，拆成两句，先把下标算到局部变量里 ([[pl-binding-evaluation-order-best-practice]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：

---
id: pl-functional-iterators-laziness-foundation-go-range-over-func
node: functional.iterators-laziness
type: qa
step: 5
---
## Q
Go 1.23 的 range-over-func 和 `iter.Seq`、`iter.Pull` 是什么？为什么 Go 选择了推送式而不是 `Iterator` 接口？

## A
Go 1.23 允许 `for ... range` 作用于**函数**：一个形如 `func(yield func(T) bool)` 的函数，就是一个迭代序列（类型别名 `iter.Seq[T]`）。函数内部调用 `yield(v)` 把每个值交给循环体；`yield` 返回 `false` 表示循环体 `break` 了，函数应当尽快返回。

```go
func Evens(n int) iter.Seq[int] {
    return func(yield func(int) bool) {
        for i := 0; i < n; i += 2 {
            if !yield(i) { return }
        }
    }
}
for x := range Evens(100) { if x > 4 { break }; fmt.Print(x, " ") }  // 0 2 4
slices.Collect(Evens(7))                                           // [0 2 4 6]
```

这是**推送**：序列自己驱动，循环体是被回调的函数。优点是序列函数里可以用普通的 `for`、`defer`、递归（遍历树时极方便），不需要手写状态机。

需要「拉取」（一次取一个）时用 `iter.Pull` 转换：

```go
next, stop := iter.Pull(Evens(7))
defer stop()           // 必须调用，否则序列函数得不到收尾的机会
fmt.Println(next())    // 0 true
```

Go 没有像 Rust 那样的 `Iterator` 接口加一堆适配器，是因为它没有泛型方法（1.27 才有）、不想在标准库里增加庞大的适配器体系，而是选了一个对语言改动最小的方案：只让 `range` 认识函数。适配器（`Map`、`Filter`）需要用户自己写成普通函数，库的集中度远低于 Rust 与 Java。

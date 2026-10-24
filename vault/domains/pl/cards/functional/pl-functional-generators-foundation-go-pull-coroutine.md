---
id: pl-functional-generators-foundation-go-pull-coroutine
node: functional.generators
type: qa
step: 3
---
## Q
Go 的 `iter.Pull` 为什么需要 `stop`？它和 Python 的生成器是什么关系？

## A
Go 没有 `yield` 关键字，但 `iter.Pull` 能把一个推送式序列函数转成「一次取一个」的形式，内部用的是**协程**：序列函数在自己的栈上运行，每次 `next()` 切换过去，跑到它调用 `yield` 为止再切回来。

```go
func count() iter.Seq[int] {
    return func(yield func(int) bool) {
        defer fmt.Println("producer cleanup")
        for i := 0; ; i++ { if !yield(i) { return } }
    }
}
next, stop := iter.Pull(count())
fmt.Println(next())    // 0 true
fmt.Println(next())    // 1 true
stop()                 // 输出 producer cleanup
fmt.Println(next())    // 0 false
```

`stop()` 的作用：告诉序列函数「别再产出了」，让它的 `yield` 返回 `false`，序列函数得以执行 `defer` 并退出。没调用就不会有收尾，序列函数永远挂在暂停点，占着资源。这与 Python 里没有 `close()` 的未耗尽生成器类似，但 Python 靠垃圾回收时自动 `close`，Go 要求显式。

与 Python 的差别在**栈的类型**：Python 的生成器是无栈的，`yield` 只能写在生成器函数自己的函数体里；Go 的协程有自己的栈，序列函数可以在任意深度的普通函数调用里调用 `yield` 回调（因为回调只是一个函数）。所以递归遍历树在 Go 里直接写递归，不需要像 Python 那样每层都 `yield from`。

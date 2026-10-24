---
id: pl-functional-closures-pitfall-late-binding-loop
node: functional.closures
type: qa
step: 10
---
## Q
在循环里创建闭包，Python 的晚绑定和 Go 1.22 之前的循环变量共享，各自会产生什么结果？

## A
两门语言犯的是同一个错：闭包捕获了**变量**，而循环里只有一个变量在不停变化。

**Python**：

```python
fs = [lambda: i for i in range(3)]
[f() for f in fs]                  # [2, 2, 2]，不是 [0, 1, 2]
gs = [lambda i=i: i for i in range(3)]
[g() for g in gs]                  # [0, 1, 2]：默认参数在定义时求值
```

三个 lambda 共享同一个 `i`，等到调用时循环早已结束，`i` 是 2。

**Go 1.21 及以前**：`for i := 0; i < 3; i++` 只有**一个** `i`。在循环里启动 goroutine 引用 `i`，等它们真正执行时，`i` 已经变成 3：

```go
for i := 0; i < 3; i++ {
    wg.Add(1)
    go func() { defer wg.Done(); mu.Lock(); got = append(got, i); mu.Unlock() }()
}
// go.mod 为 go 1.21：输出 [3 3 3]
// go.mod 为 go 1.27：输出 0、1、2 各一次（顺序不定），例如 [2 0 1]
```

Go 1.22 把语义改成**每次迭代一个新变量**，而且改动由 `go.mod` 里的 `go` 版本决定：旧模块保持旧行为，新模块得到新行为。这是语言为了纠正一个被证明几乎总是出错的设计，付出了破坏兼容的风险，换来大量 bug 的消失。

诊断信号：回调里读到的总是最后一个值；日志里同一个 ID 重复出现。修法：Python 用默认参数、`partial`，Go 在旧版本里写 `i := i` 或把 `i` 作为参数传入。Java 和 Rust 不会有这个问题：前者复制值，后者要么 `move` 要么借用检查失败。

C++ 没有晚绑定，因为捕获方式是显式的；但它有对偶的陷阱：`[&]` 捕获的是引用，闭包活得比变量久就悬空，而且编译器不报：

```cpp
std::function<int()> make() {
    int n = 42;
    return [&] { return n; };   // [&]: capture n by reference
}                               // n is destroyed here
// main: std::printf("%d\n", make()());
```

`clang++ -std=c++23 -Wall -Wextra` 零警告，运行输出 `42`（读到了已经失效的栈内存，碰巧还没被覆盖）。加 `-fsanitize=address` 并设 `ASAN_OPTIONS=detect_stack_use_after_return=1` 才报：`ERROR: AddressSanitizer: stack-use-after-return`。修法：会逃出作用域的闭包写 `[n]` 拷贝，或 `[n = std::move(x)]` 搬入。

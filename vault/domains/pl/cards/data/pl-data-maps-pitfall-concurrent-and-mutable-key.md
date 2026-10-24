---
id: pl-data-maps-pitfall-concurrent-and-mutable-key
node: data.maps-collections
type: qa
step: 11
---
## Q
映射在线上最常见的两类事故是什么？Go 的并发写和 Java 的可变键各自的真实表现是什么，怎样防？

## A
**Go：并发写直接让进程退出**。四个 goroutine 同时往同一个 map 写：

```go
m := map[int]int{}
for g := 0; g < 4; g++ {
    go func() { for i := 0; i < 100000; i++ { m[i] = i } }()
}
```

真实输出：`fatal error: concurrent map writes`，随后是一串运行时栈。这不是 `panic`，`recover` 无法拦截，整个服务进程退出。运行时用一个标志位做廉价检测，抓到就终止，而不是让数据结构悄悄损坏。要注意检测是尽力而为的：并发读写有时不会被抓到，会出现错乱数据。

**防线**：每个共享的 map 配一个 `sync.RWMutex`，并把 map 与锁封装在同一个类型里，不暴露裸 map；在 CI 里用 `go test -race` 抓数据竞争。

**Java：可变键让条目隐形**。把对象放进 `HashMap` 后修改了参与 `hashCode` 的字段，真实结果是 `get(k)` 返回 `null`，`size()` 仍为 1：条目还在表里，却再也找不到，也不会被清理，造成内存泄漏和逻辑错误（比如缓存永远不命中）。

**防线**：键用不可变类型；用 `record` 当键；评审时对 `HashMap<自定义类, ...>` 检查那个类有没有可变字段进入 `hashCode`。

**Python 的同类事故**：`dict` 键被 `__hash__` 保护，列表不能当键，所以更早失败；但自定义类如果定义了基于可变字段的 `__hash__`，同样会出现隐形条目。

**共同教训**：映射的正确性依赖键的稳定性和访问的串行化，而这两者在语言层面都只有部分保护。

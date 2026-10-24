---
id: pl-memory-stack-heap-go-growable-stack
node: memory.stack-heap
type: qa
step: 7
---
## Q
同样做 1000 万层递归，Go、Java、Python 的结果为什么差这么大？Go 的栈有什么独特设计？

## A
同一个简单递归函数（每层加 1）的一次本机实测：

```console
Go      depth(10_000_000)  -> 10000000
Java    默认栈               -> StackOverflowError，约 4.4 万层
Python  默认设置             -> RecursionError，上限 1000 层
```

三种做法：
- Java 线程栈在创建时就保留固定大小（默认约 1 MB 量级，用 `-Xss` 调），用满就抛 `StackOverflowError`。
- Python 不看内存，而是数调用深度：`sys.getrecursionlimit()` 默认 1000，超过抛 `RecursionError`，用来在 C 栈真的崩溃之前拦住。
- Go 每个 goroutine（Go 的轻量协程）的栈从很小（KB 量级）开始，函数入口检查剩余空间，不够就分配一块更大的连续内存、把旧栈整体复制过去并修正指针，称为可增长栈（growable stack）。上限在 64 位上默认 1 GB。

这个设计的意义是：goroutine 创建几乎不占内存，所以可以开几十万个；代价是栈上的指针必须能被运行时找到并改写，所以 Go 不允许你把栈地址存进不受管理的内存，也是逃逸分析必须保守的原因之一。

Rust 的线程栈同样是固定大小（主线程通常 8 MB，`std::thread::spawn` 默认 2 MiB），Rust 为了零成本不提供自动增长。

---
id: pl-memory-stack-heap-foundation-heap-allocation
node: memory.stack-heap
type: qa
step: 3
---
## Q
堆（heap）分配是什么？在 Java、Go、Rust、Python 里，各用什么写法把一个值放到堆上？

## A
堆是一大片由分配器（allocator）管理的内存。程序要一块多大的空间，分配器就从中切出一块，返回它的地址；这块内存会一直保留，直到有人归还（手动释放，或由垃圾回收器 garbage collector，简称 GC，在后台发现没人再用时自动归还）。栈帧随函数返回消失，而堆上的内存可以活得比创建它的函数更久，也可以在运行期才确定大小，代价是分配和回收都比栈慢，访问还要多经过一次指针。

四种语言“向堆要内存”的入口：
- **Java**：`new Point(1, 2)` 总是在堆上创建对象，变量里存的是指向它的引用（reference，一个地址）。
- **Go**：`&Point{1, 2}`、`new(T)`、`make([]int, n)` 看起来是在要堆内存，但最终放哪里由编译器决定（逃逸分析 escape analysis：编译器分析指针是否会离开当前函数，不会离开就留在栈上）。
- **Rust**：`Box::new(x)` 把一个值放到堆上，`Vec`、`String` 内部也用堆存放内容；没有这些类型就都在栈上，写法即成本。
- **Python**：所有对象都在堆上，变量只是指向对象的名字。

一个小场景：Java 里 `Point p = new Point(1, 2);` 会在栈帧里留一个 8 字节左右的引用 `p`，在堆上创建 Point 对象；函数返回后栈上的 `p` 消失，但如果别处还有引用指向这个对象，它仍然存在，直到 GC 发现没有引用了才回收。

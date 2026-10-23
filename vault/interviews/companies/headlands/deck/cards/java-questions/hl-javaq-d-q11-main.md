---
id: hl-javaq-d-q11-main
node: java-questions.d-memory
type: qa
step: 2
---
## Q
Java 里执行 `new Foo()` 时发生了什么？分配有多快，之后的代价是什么？
What happens on `new Foo()` in Java? How fast is Java allocation, and what does it cost later?

## A
一句话：Java 的 `new` 在线程私有的 **TLAB**（线程本地分配缓冲，thread-local allocation buffer，Eden 里一块线程私有区域）里做**指针碰撞**（几条指令），内存已清零，再写对象头，再跑构造器。

- 快是因为 GC 是**复制 / 整理式**的：回收时把存活对象搬走，剩下整块空间当空闲，分配永远是"顶指针前移"，没有碎片，不搜索空闲链表。
- 代价**后移到 GC**：分配速率越高，young GC 越频繁。
- 没逃逸的对象会被 JIT 消除；大对象（G1 里超过 region 一半的 humongous）和超大数组走慢路径，别在热路径上分配。

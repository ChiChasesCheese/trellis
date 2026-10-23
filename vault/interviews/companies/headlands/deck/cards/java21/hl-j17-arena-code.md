---
id: hl-j17-arena-code
node: java21.j17-ffm-api
type: qa
step: 6
---
## Q
写出用 `Arena.ofConfined()` 分配 32 字节、8 字节对齐的内存段的代码。新分配的内存里是什么？`close()` 之后访问会怎样？

## A
```java
try (Arena arena = Arena.ofConfined()) {
    MemorySegment seg = arena.allocate(32, 8);   // 32 字节，8 字节对齐；已清零
    ...
}   // close()：这块内存立刻归还
```
- 新分配的内存**保证清零**（第一个 `long` 读出为 0），所以可以用「全零 = 空槽」。
- 关闭后访问 `seg` 抛 `IllegalStateException: Already closed`，不会崩进程；`seg` 引用不是 `null`，只是访问抛异常。
- 底层是 `malloc`/`posix_memalign` 类调用，`close()` 是 `free`，JVM 里没有对应堆对象，GC 不扫描。

---
id: hl-j17-close-responsibility
node: java21.j17-ffm-api
type: qa
step: 18
---
## Q
Arena 的 `close()` 责任是什么？忘了会怎样？为什么堆外 map 的 `close()` 要写 `isAlive()` 检查？

## A
忘了 `close()`（`ofConfined`/`ofShared`）= **内存泄漏**，GC 帮不了你；`ofAuto()` 由 GC 回收但时机不确定。所以用 `try-with-resources`。

`Arena.close()` 二次调用会抛异常，所以堆外 ticker map 的 `close()` 写成 `if (arena.scope().isAlive()) arena.close();`。

关闭后的 `MemorySegment` 引用不是 `null`，访问抛 `IllegalStateException`：安全（不崩）但是运行时错误；别把 segment 存进比 arena 活得更久的对象。

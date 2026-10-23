---
id: hl-j17-ex1-safety
node: java21.j17-ffm-api
type: qa
step: 15
---
## Q
对一个 32 字节的 segment 做访问：越界、arena 关闭后访问、shared arena 跨线程、confined arena 跨线程，分别发生什么？

## A
- 越界 → `IndexOutOfBoundsException`；
- arena 关闭后访问 → `IllegalStateException: Already closed`；
- `ofShared` arena：另一线程写入 99，主线程读到 99；
- `ofConfined` arena：别的线程访问 → `WrongThreadException`；
- 新分配的第一个 `long` 为 0（`byteSize = 32`）。

这些都是确定的异常，而不是读垃圾或崩溃。

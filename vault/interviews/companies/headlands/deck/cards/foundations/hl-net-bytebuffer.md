---
id: hl-net-bytebuffer
node: foundations.networking-basics
type: qa
step: 33
---
## Q
`ByteBuffer` 的 position、limit、capacity 是什么？`flip()`、`clear()`、`compact()` 各用于什么场景？

## A
三个游标：**position** 下一个读 / 写位置，**limit** 可操作区域末端，**capacity** 总容量。

以容量 8 为例：`allocate(8)` 时 position 0、limit 8；`channel.read` 读入 5 字节后 position 5；`flip()` 后 position 0、limit 5，可以读 0 到 5；读走 3 字节后 position 3，剩 2 字节是不完整的消息；`compact()` 把剩余 2 字节挪到开头，position 2、limit 8，切回继续写入。

- `flip()`：写完准备读（limit = position; position = 0）；
- `clear()`：读完准备重新写，丢弃一切；
- `compact()`：读了一部分，保留未读部分继续写，**处理半包的标准工具**。

直接缓冲区（`allocateDirect`）分配在堆外，I/O 少拷贝一次，但分配释放更贵，应分配一次长期复用。

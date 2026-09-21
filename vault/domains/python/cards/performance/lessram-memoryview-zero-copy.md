---
id: lessram-memoryview-zero-copy
node: performance.less-ram
type: qa
source: python-docs
---
## Q
`memoryview(obj)` 和直接对同一个 `bytes`/`bytearray` 做切片 `obj[1:4]` 相比，为什么前者不会产生额外的内存拷贝？

## A
`memoryview` 只是引用了支持缓冲区协议（buffer protocol）对象的底层内存，自己不拥有数据；对 `memoryview` 再切片得到的还是引用同一块内存的新 view，而对 `bytes`/`bytearray` 切片会立刻分配新对象把数据复制一份。需要真正独立的拷贝时才调用 `.tobytes()` 或 `bytes(view)`。

---
id: memoryview-zero-copy-buffer-protocol
node: model.sequences
type: qa
source: python-docs
---
## Q
`memoryview(obj)` 是如何做到「访问 `obj` 的内部数据但不复制」的？对 memoryview 切片（如 `v[1:4]`）得到的结果和直接对 `obj` 切片有什么本质不同？

## A
`memoryview` 要求 `obj` 支持缓冲区协议（buffer protocol，内建的 bytes、bytearray 等都支持），创建时只记录指向 `obj` 底层内存的一份视图元数据（起始地址、元素个数、每个元素的字节数等），不拷贝任何数据。对 memoryview 切片得到的仍然是一个新的 memoryview 子视图，同样不拷贝底层数据；而对 bytes 这类对象直接切片会生成一份新的独立数据。如果确实需要拷贝出一份独立数据，要显式调用如 `bytes(v[1:4])`，才会真正复制出新对象。

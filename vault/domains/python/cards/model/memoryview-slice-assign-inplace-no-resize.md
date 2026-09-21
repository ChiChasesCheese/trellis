---
id: memoryview-slice-assign-inplace-no-resize
node: model.sequences
type: qa
source: python-docs
---
## Q
对一个指向可写缓冲区（如 bytearray）的 memoryview 做切片赋值，如 `v[1:4] = b'123'`，会发生什么？为什么给一个长度不匹配的切片赋值（如 `v[2:3] = b'spam'`）会报错？

## A
因为 memoryview 是对底层缓冲区的视图而非拷贝，`v[1:4] = b'123'` 会直接就地修改底层 bytearray 对应位置的数据，不产生新对象。但 memoryview 不允许通过切片赋值改变自己映射的字节数（不能 resize）：`v[2:3]` 只圈定了 1 个字节的范围，赋值 `b'spam'`（4 字节）时左值和右值的长度（结构）不一致，会直接抛出 `ValueError`，必须让赋的新值和被替换的切片长度完全一致。

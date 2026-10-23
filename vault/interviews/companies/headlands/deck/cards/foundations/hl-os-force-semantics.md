---
id: hl-os-force-semantics
node: foundations.os-processes-threads-ipc
type: qa
step: 47
---
## Q
`MappedByteBuffer.force()` 做了什么？进程崩溃时已写到映射区但没 `force()` 的数据会丢吗？

## A
`force()` 对映射区调用 `msync`，请求内核把脏页写到存储设备。

写到映射区的数据先落在内核页缓存里，进程崩溃后这些页仍在，之后由内核写回，所以**进程崩溃不会丢**；机器断电或内核崩溃才丢未写回的页。抗断电要 `force()`，并保证设备写缓存落盘。

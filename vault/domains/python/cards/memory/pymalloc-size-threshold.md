---
id: pymalloc-size-threshold
node: memory.allocator
type: qa
tags: [grown]
source: python-docs
---
## Q
一次内存分配请求，多大以下会交给 pymalloc 处理，多大以上会直接走系统的 `malloc`？

## A
请求 ≤512 字节时由 pymalloc 接管：按固定的 size class（大小类，64 位平台以 16 字节为粒度分档，共 32 档）从对应 pool 里切一个 block 出来，不直接调用系统分配器；超过 512 字节的请求（大 list/dict 的底层数组、长字符串等）绕过 pymalloc，直接调用系统的 `malloc`/`free`。

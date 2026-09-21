---
id: pymalloc-three-tiers
node: memory.allocator
type: cloze
tags: [grown]
source: python-docs
---
CPython 的小对象分配器 pymalloc 从大到小分三层：{{c1::arena（竞技场，约 1 MiB，一次性向系统申请的大块内存）}} → {{c2::pool（池，64 位平台 16 KiB、32 位 4 KiB，一个 pool 只服务同一个 size class）}} → {{c3::block（固定大小的小块，真正分配给对象的内存单元）}}。

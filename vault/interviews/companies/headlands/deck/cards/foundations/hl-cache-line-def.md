---
id: hl-cache-line-def
node: foundations.cpu-cache-locality
type: qa
step: 6
---
## Q
缓存行（cache line）是什么？x86 和 Apple 芯片上各是多大？为什么要按行搬运？

## A
CPU 不是一个字节一个字节地读，而是**一次读一整行**。x86 和大多数 ARM 服务器核的缓存行是 **64 字节**，**Apple 芯片是 128 字节**（macOS 上 `sysctl hw.cachelinesize` 可查）。「64 字节」是常见值而不是定律，面试说「通常 64，Apple M 系列是 128」会显得你真测过。

按行搬的原因：DRAM 打开一行后连续传输多个字很便宜，但「开一行」本身很贵，所以一次取 64 字节比取 8 次 8 字节划算得多。

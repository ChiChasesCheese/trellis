---
id: hl-cq-q32-mmap-experiment
node: cpp-questions.h-os
type: qa
step: 2
---
## Q
`mmap` 512 MB 匿名内存后，缺页数和常驻内存（RSS）是多少？每页写一个字节之后呢？页大小是多少？

## A
- 映射 512 MB 之后：缺页 **+0**，最大 RSS 约 **1 MB**。
- 每页碰一个字节之后：缺页 **+32768**（= 32768 页），RSS 涨到约 **513 MB**。
- 页大小：实测 Apple 芯片 16 KB（x86 Linux 通常 4 KB）；32768 页 × 16 KB = 512 MB。
- 含义：映射只是登记，只有真正触碰才付出物理内存代价。

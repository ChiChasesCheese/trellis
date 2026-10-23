---
id: hl-javaq-g-q35-say60
node: java-questions.g-os
type: qa
step: 15
---
## Q
用英文 60 秒回答：Explain virtual memory, the page cache and page faults. Why is a JVM's RSS bigger than `-Xmx`?

## A
结构：虚拟地址经页表映射、缺页由内核补页 → 文件 I/O 经 page cache → RSS 大于 Xmx 的原因（元空间、代码缓存、栈、GC 簿记、直接内存）→ 实测 314 MB → 低延迟用预触碰并避免 swap。

> "Each process has a virtual address space that the MMU maps to physical pages through page tables, with the TLB caching translations. Touching an unmapped page triggers a page fault and the kernel supplies a zeroed page or reads the file in. File I/O goes through the page cache, so writes are buffered until writeback or an fsync. A JVM's resident memory is more than `-Xmx` because it also holds metaspace, the code cache, thread stacks, GC bookkeeping, direct buffers and shared libraries - on a test JVM with a 256 MB heap I saw about 314 MB resident, with roughly 58 MB of that being GC structures, according to native memory tracking. For latency, I'd pre-touch the heap so page faults happen at start-up, and avoid swap."

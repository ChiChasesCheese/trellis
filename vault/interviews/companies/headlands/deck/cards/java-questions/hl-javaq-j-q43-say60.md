---
id: hl-javaq-j-q43-say60
node: java-questions.j-storage
type: qa
step: 9
---
## Q
用英文 60 秒回答：What happens when you `write()` to a file? What are the page cache and `fsync`? How do you make writes durable and fast?

## A
结构：write 只进 page cache，fsync 才持久 → 实测 7 ms、6 秒、30 ms → 组提交摊薄成本 → 追加式 WAL、顺序 I/O、预分配、sync 后才确认 → 绝对数字随设备变，比例成立。

> "`write` copies into the kernel page cache and returns; the data is only durable after `fsync`, which in Java is `FileChannel.force`. That's why you can't confuse a fast write with a safe one. On my laptop 2,000 4-KB appends took 7 ms without syncing, about 6 seconds when I forced after every record - roughly three milliseconds each - and 30 ms when I forced once at the end. That gap is why storage systems use group commit: many records share one fsync, so you keep durability but amortise the cost, trading a little latency. The usual design is an append-only write-ahead log, sequential I/O, preallocated files, and only acknowledging after the sync. The absolute numbers depend on the device and OS - Linux with a power-loss-protected NVMe is much faster - but the ratios hold."

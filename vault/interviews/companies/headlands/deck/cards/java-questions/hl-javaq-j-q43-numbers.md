---
id: hl-javaq-j-q43-numbers
node: java-questions.j-storage
type: qa
step: 2
---
## Q
2000 条 4 KB 记录：只写 page cache、每条都 force、全部写完再一次 force、mmap 写加一次 force，各用多少毫秒？说明了什么？

## A
- 只 write（page cache）：**7 ms**。
- 每条记录后 `force()`：**6286 ms**，每条约 3 ms。
- 全部写完，结尾一次 `force()`：**30 ms**。
- mmap store + 结尾一次 `force()`：**16 ms**。
- 重读刚写的 31 MB：11 ms（来自 page cache）。

每条都 fsync 比只写 page cache **慢约 900 倍**；攒一批再 fsync 只慢约 4 倍——这就是 **group commit**（数据库、Kafka 的刷盘策略）：用"几毫秒内的一批共享一次 fsync"换吞吐，延迟只增加一点点。

这些数字来自 macOS；Linux + 带断电保护的 NVMe 上单次 fsync 可以是几十到几百微秒。**只看比例，不要把毫秒数当通用结论。**

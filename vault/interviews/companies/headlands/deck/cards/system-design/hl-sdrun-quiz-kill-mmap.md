---
id: hl-sdrun-quiz-kill-mmap
node: system-design.how-to-run
type: qa
step: 35
---
## Q
口头自测：`kill -9`、机器掉电、机房断网三种故障下，`mmap` 日志分别还剩什么？光纤 1 km 多少 µs？co-location 把往返从 7 ms 降到什么数量级？

## A
- `kill -9`：数据在页缓存里，**还在**，内核之后写回，不需要 fsync；
- 机器掉电：未写回的脏页**会丢**，需要 fsync 或复制到另一台机器；
- 机房断网：本机日志在，但无法复制到异地，也连不上交易所，要靠与交易所对账恢复；
- 光纤 1 km 约 **5 µs**；co-location 把往返从跨城约 7 ms（芝加哥–纽约光纤）降到**几微秒**量级。

---
id: hl-sd03-fu-fsync
node: system-design.sd03-low-latency-trading
type: qa
step: 41
---
## Q
追问：日志要 fsync 吗？热路径等不等？

## A
热路径只写内存环，Journaler 异步追加到 mmap 文件。进程崩溃：页缓存里数据还在，不需要 fsync；掉电 / 内核崩溃：需要 fsync 或已复制到另一台机器；机房故障：靠交易所 / 清算行对账。fsync 在 NVMe 上几十 µs 到 ms 不定，不能放进 µs 预算；日志环满 ⟹ 告警 / 熔断，而不是丢事件。区分「交易所自己的撮合引擎必须先落日志再处理」与「客户端以交易所为真相」。

可以说：「持久性分三档，我只为热路径付最便宜的一档，剩下的靠复制和对账。」

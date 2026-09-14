---
id: kafka-consumer-auto-commit-duplicate-window
node: consumer.offset-commit
type: qa
source: kafka-2e
---
## Q
把 `enable.auto.commit` 设为 true（默认值）后，消费者每隔 `auto.commit.interval.ms`（默认5秒）自动提交一次偏移量。如果消费者在两次自动提交之间的第3秒崩溃，会发生什么？调小提交间隔能不能彻底避免这个问题？

## A
接管这个分区的新消费者会从最后一次自动提交的偏移量开始读取，但那个偏移量已经落后了大约3秒，所以这3秒内处理过的消息会被重新读取一遍、重复处理。调小 `auto.commit.interval.ms` 能缩短这个「重复处理窗口」的长度，但没办法彻底消除，因为提交本身仍然是按固定时间间隔进行的，而不是每处理一条就提交一次；自动提交也无法知道当前批次里具体哪些消息已经处理完，只能整批一起提交。

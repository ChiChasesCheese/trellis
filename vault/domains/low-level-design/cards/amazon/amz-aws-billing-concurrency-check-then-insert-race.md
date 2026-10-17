---
id: amz-aws-billing-concurrency-check-then-insert-race
node: amazon.amz-aws-billing
type: qa
step: 8
tags: [grown]
---
## Q
在 AWS 账单服务里，多个线程同时上报用量，会出什么并发问题？怎样防止？

## A
去重是「查编号是否存在，再写入」两步，GIL 只保证单条字节码原子。两个线程同时上报同一个 `usage_id`，都看到「还没有」，各写一次，客户被重复计费。做法：`UsageLedger.add` 用一把 `threading.Lock` 罩住整个检查加写入，计数 `duplicates_ignored` 也在锁里读；`between` 返回元组快照，不把内部字典交出去。8 个线程同时上报同一编号，恰好 1 个返回 `True`。

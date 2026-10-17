---
id: amz-occupancy-tracker-concurrency-validate-and-append-under-one-lock
node: amazon.amz-occupancy-tracker
type: qa
step: 9
tags: [grown]
---
## Q
在办公室人数追踪里，多个闸机同时上报事件，会出什么并发问题？怎样防止？

## A
写入是「校验加追加三处」（全局时间线、区域时间线、每人最近事件）的复合操作，GIL 只保证单条字节码原子。两个线程可能都通过「时间没倒流」的校验，再交错追加，让时间数组乱序、数组长度不一致。做法：`_record` 整个在一把 `threading.Lock` 里，读也在锁里，保证读到等长的数组。吞吐更高时，每个闸机一个队列，单个消费者按时间归并后写入（单写者），锁也不需要。8 个线程各入场 50 人，总数 400，不丢。

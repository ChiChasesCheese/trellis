---
id: amz-train-fare-concurrency-lock-read-compute-write
node: amazon.amz-train-fare
type: qa
step: 8
tags: [grown]
---
## Q
在 Amazon 火车票价设计里，同一乘客的多个行程同时记账，会出什么并发问题？用什么结构防止？

## A
「读已付、算实付、写回」是三步，GIL 只保证单条字节码原子。两个线程同时读到已付 0，各自算出可付 600，各写 600，总共收了 1200，突破封顶 600。做法：`DailyCapLedger` 用一把 `threading.Lock` 罩住整个读—算—写，持锁只有微秒；`Route` 另有自己的锁，保证加站与查价不会读到半个更新。`charge` 在锁外调 `quote`，两把锁不嵌套，因此不会死锁。

---
id: amz-task-scheduler-worker-pool-and-blocking
node: amazon.amz-task-scheduler
type: qa
step: 6
tags: [grown]
---
## Q
在任务调度器设计里，如果某个任务阻塞了 10 秒（比如等网络），后面的任务会怎样？怎么改？

## A
调度线程自己执行任务时，一个阻塞任务会让所有后续任务全部延后。改法：调度线程只负责到点分发，任务交给有界线程池执行。池大小怎么定：CPU 密集型约等于核数，IO 密集型可以更多；池满时选排队（队列要有界）或拒绝。任务里的异常必须在 worker 内捕获并记录，否则线程死掉，池越用越小。关闭时区分「等已排队的任务跑完」和「立即停止」。

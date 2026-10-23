---
id: hl-os-ipc-latency-ranking
node: foundations.os-processes-threads-ipc
type: qa
step: 45
---
## Q
管道、Unix 域套接字、共享内存，哪个延迟最低？哪个最容易用？

## A
**共享内存**延迟最低：建立后读写无系统调用、无内核拷贝。管道和 Unix 域套接字每条消息两次系统调用、两次拷贝，微秒级。

最容易用的是管道（Shell 的 `|`），其次 Unix 域套接字（API 与 TCP 相同）；共享内存最难：同步、内存序、崩溃恢复都要自己做。

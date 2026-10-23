---
id: hl-os-qa-mmap-vs-read
node: foundations.os-processes-threads-ipc
type: qa
step: 40
---
## Q
面试题：`mmap` 和 `read` 的区别？什么时候用 `mmap`？

## A
推荐答法：「`read` 把页缓存数据拷贝到用户缓冲区，每次一次系统调用；`mmap` 让页表直接指向页缓存，访问无系统调用也无拷贝，首次访问触发缺页。适合随机访问大文件、多进程共享、需要持久化的消息日志。要注意字节序、文件截断导致的 `SIGBUS`、刷盘语义（`force`）。」

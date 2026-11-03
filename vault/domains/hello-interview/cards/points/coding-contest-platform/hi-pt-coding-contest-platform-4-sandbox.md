---
id: hi-pt-coding-contest-platform-4-sandbox
node: qb.sd.coding-contest-platform.points
type: qa
step: 4
---
## Q
**在线判题与编程竞赛平台 · 不可信代码的沙箱**｜必会 · 出自：在线判题与编程竞赛平台 › 深入 1

怎样安全运行用户代码？容器要做哪些加固？为什么公开平台还要在容器之上再加一层？

## A
**不可接受。** 在 API 进程里直接运行：可删数据、挖矿、死循环拖垮服务。
**容器加固。** 代码目录只读、输出写临时目录；cgroup 限 CPU、内存、进程数；每点墙钟/CPU 时间上限（如 5 秒）超时杀进程；关网络；seccomp 只放行几十个系统调用。
**更强。** 容器共享内核、有逃逸漏洞，再加 gVisor 或 Firecracker，用少量启动开销换内核隔离。

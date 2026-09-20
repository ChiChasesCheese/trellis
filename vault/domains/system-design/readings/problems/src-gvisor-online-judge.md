---
nodes: [problems.realtime.online-judge]
url: https://gvisor.dev/docs/architecture_guide/performance/
---
# gVisor — Performance Guide

值得读：gVisor 官方文档说明其用户态内核（Sentry）拦截系统调用的开销主要落在系统调用
密集/IO 密集型负载上，CPU 密集型代码基本不受影响——这正好是判题代码的典型特征。本题解
用这一点把 gVisor 定位为容器和 Firecracker 之间的中间选项，但因为它依然和宿主机共享
同一个内核、不是独立的虚拟化边界，本题解最终为对外匿名提交选择了 Firecracker 而不是
gVisor，仅把 gVisor 作为一个值得记录的备选方案。

---
id: problems-online-judge-firecracker-vs-container-vs-gvisor
node: problems.realtime.online-judge
type: qa
step: 2
tags: [grown]
---
## Q
In an online judge design that must run anonymous, untrusted user code with zero tolerance for sandbox escape, why does a Firecracker microVM (one per submission) get chosen over a plain container (namespaces + cgroups + runc) or gVisor, given Firecracker's own published numbers of under 125ms boot time and under 5MiB memory overhead per microVM?

## A
A plain container shares the host kernel directly, so a kernel privilege-escalation bug lets an escape reach the host — too thin a boundary for anonymous, adversarial code. gVisor's Sentry intercepts syscalls in userspace, narrowing the attack surface, but still runs on and shares the same host kernel, so it isn't an independent hardware boundary. Firecracker instead boots a minimal KVM-backed virtual machine per submission, so escape requires breaking KVM itself rather than an application-layer syscall filter — and because it boots in under 125ms with under 5MiB overhead, running one disposable microVM per submission stays cheap enough to support thousands of them densely packed on a host.

## Q zh
在一个必须运行匿名、不可信用户代码、且对沙箱逃逸零容忍的在线判题系统设计中，为什么最终选择'每次提交一个 Firecracker microVM'，而不是普通容器（namespaces + cgroups + runc）或 gVisor？（Firecracker 官方数字：启动时间 < 125ms，每个 microVM 内存开销 < 5MiB）

## A zh
普通容器直接和宿主机共享内核，一旦内核存在提权漏洞，逃逸后就能直接危及宿主机——对匿名、高对抗性的代码而言这道边界太薄。gVisor 的 Sentry 在用户态拦截系统调用，收窄了攻击面，但依然运行在同一个宿主机内核上，不是一个独立的硬件级边界。Firecracker 则为每次提交启动一台基于 KVM 的极简虚拟机，逃逸需要突破 KVM 本身而不是应用层的系统调用过滤；又因为它启动时间 < 125ms、开销 < 5MiB，每次提交用完即弃一个 microVM 依然便宜到可以在单机上密集打包成千个。

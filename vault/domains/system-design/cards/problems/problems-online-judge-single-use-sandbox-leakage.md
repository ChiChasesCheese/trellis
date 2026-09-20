---
id: problems-online-judge-single-use-sandbox-leakage
node: problems.realtime.online-judge
type: qa
step: 7
tags: [grown]
---
## Q
In an online judge design, why must every sandbox be destroyed after a single submission rather than reused across submissions, and how does the sandbox choice from the isolation deep dive make this affordable?

## A
Reusing a sandbox across submissions risks one tenant's code reading filesystem or memory residue left by a previous tenant's execution — a cross-submission information leak, which is unacceptable when submissions are mutually untrusted. The fix is to destroy the sandbox after every run and start fresh for the next one. This is only cheap because the sandbox is a Firecracker microVM that boots in under 125ms and costs under 5MiB of memory overhead — a traditional, slower-booting VM would make 'destroy after every submission' a real performance tax instead of a nearly-free security guarantee.

## Q zh
在一个在线判题系统设计中，为什么每个沙箱都必须在一次提交后销毁、不能跨提交复用？隔离机制这一深入探讨里的沙箱选型为什么让这个做法负担得起？

## A zh
跨提交复用沙箱会有一个租户的代码读到上一个租户执行残留在文件系统或内存里的痕迹的风险——这是提交之间互不信任的场景下无法接受的信息泄露。解决办法是每次跑完就销毁沙箱，下一次提交重新起一个全新的。这之所以便宜，是因为沙箱选的是启动时间 < 125ms、内存开销 < 5MiB 的 Firecracker microVM——如果用传统的、启动慢得多的虚拟机，'每次提交后销毁'就会变成实打实的性能税，而不是近乎免费的安全保证。

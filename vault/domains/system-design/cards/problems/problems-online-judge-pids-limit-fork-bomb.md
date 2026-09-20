---
id: problems-online-judge-pids-limit-fork-bomb
node: problems.realtime.online-judge
type: qa
step: 4
tags: [grown]
---
## Q
In an online judge design, why can a submission that stays within its CPU and memory limits still take down a judge host, and what specifically prevents it?

## A
A fork bomb repeatedly spawns child processes without necessarily using much CPU or memory per process, exhausting the host's process table and scheduler capacity rather than its CPU or memory quota — so CPU and memory limits alone don't stop it. The fix is the cgroup pids controller, which caps the total number of processes/threads a cgroup may create (e.g. 32) independently of the CPU and memory limits; all three limits must be configured together, since a submission compliant on CPU and memory but unbounded on process count would bypass the other two.

## Q zh
在一个在线判题系统设计中，为什么一份 CPU 和内存都没有超限的提交，依然可能拖垮整台判题主机？具体靠什么机制阻止这种情况？

## A zh
fork bomb 通过不断派生子进程发起攻击，每个子进程本身未必消耗多少 CPU 或内存，而是耗尽宿主机的进程表和调度器容量——仅靠 CPU 和内存限额挡不住这种攻击。解决办法是 cgroup 的 pids 控制器，它独立于 CPU 和内存限额之外，单独限制一个 cgroup 能创建的进程/线程总数（例如上限 32）；三类限额必须同时配置，否则一份 CPU 和内存都合规、但进程数不受限的提交就能绕过另外两道限额。

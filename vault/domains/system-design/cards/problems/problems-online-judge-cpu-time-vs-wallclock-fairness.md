---
id: problems-online-judge-cpu-time-vs-wallclock-fairness
node: problems.realtime.online-judge
type: qa
step: 3
tags: [grown]
---
## Q
In an online judge design, why should Time Limit Exceeded (TLE) be judged against CPU time measured from a cgroup's cpu.stat rather than wall-clock time, and why is a separate, much looser wall-clock ceiling still required on top of that?

## A
If TLE were judged by wall-clock time, the same submission could pass when the host is idle and fail purely from scheduling contention when the host is busy, violating fairness — identical code should get identical verdicts regardless of when it runs. Measuring CPU time instead ties the verdict only to the computation the code actually performed. But CPU time alone lets a submission sleep or wait on a never-ready connection indefinitely while consuming almost no CPU, occupying a sandbox slot without triggering the CPU limit — so a separate wall-clock cap (e.g. 3-5x the CPU limit) is still needed as a backstop.

## Q zh
在一个在线判题系统设计中，为什么超时（Time Limit Exceeded, TLE）的判定应该用 cgroup 的 cpu.stat 统计出的 CPU 时间，而不是墙钟时间（wall-clock time）？为什么在此基础上还需要一个宽松得多的独立墙钟时间上限？

## A zh
如果按墙钟时间判 TLE，同一份提交在宿主机空闲时能通过，在宿主机繁忙时却可能纯粹因为调度争抢而超时，违反公平性——相同代码在任何时候运行都应该得到相同判定。改用 CPU 时间可以让判定只取决于代码实际执行的计算量。但只用 CPU 时间的话，一份代码可以通过无限期 sleep 或等待一个永不就绪的连接、几乎不消耗 CPU 却长期占用一个沙箱槽位，不会触发 CPU 限额——因此仍需要一个宽松得多的独立墙钟时间上限（例如 CPU 限额的 3–5 倍）作为兜底。

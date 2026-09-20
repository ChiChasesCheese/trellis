---
nodes: [problems.realtime.online-judge]
url: https://github.com/ioi/isolate
---
# isolate — Sandbox for securely executing untrusted programs

值得读：IOI（International Olympiad in Informatics）官方 CMS（Contest Management
System）采用的学术竞赛沙箱，基于 Linux namespaces 与 cgroups，不引入虚拟机层，由
Martin Mareš 主导维护。本题解把它作为"内部可信/低对抗性场域"隔离方案的代表，和 nsjail
归为同一信任等级，并说明为什么本设计面向匿名公开、可达十万人规模的竞赛时没有直接照搬
它的路线，而是选择了隔离强度更高的 Firecracker microVM。

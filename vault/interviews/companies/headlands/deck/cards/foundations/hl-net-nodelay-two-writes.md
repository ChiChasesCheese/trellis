---
id: hl-net-nodelay-two-writes
node: foundations.networking-basics
type: qa
step: 49
---
## Q
判断：「设置了 `TCP_NODELAY`，把 header 和 body 分两次 `write` 也没问题。」

## A
不完全对。没有 Nagle 的 40 ms 停顿了，但两次 `write` 变成**两个小 TCP 段、两次系统调用**，对端还可能要处理半包。

更好的做法是合并到一个缓冲区一次写，或用 `writev` 聚集写：少一次系统调用、少一个包。

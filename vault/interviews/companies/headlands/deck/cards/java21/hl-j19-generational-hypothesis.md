---
id: hl-j19-generational-hypothesis
node: java21.j19-runtime-zgc-jit
type: qa
step: 3
---
## Q
分代假说（generational hypothesis）是什么？据此堆怎么分？

## A
**绝大多数对象很快就死**（临时字符串、迭代器、请求对象），少数活得很久（缓存、订单簿）。

所以把堆分成：
- **年轻代**（young）：新对象，常回收，便宜；
- **老年代**（old）：长寿对象，偶尔回收，贵。

这是 G1 和分代 ZGC 的共同基础。

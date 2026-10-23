---
id: hl-cache-coherence-mesi
node: foundations.cpu-cache-locality
type: qa
step: 21
---
## Q
多核 CPU 的缓存一致性（cache coherence）协议 MESI 是什么？一致性的粒度是什么？

## A
每个核有自己的 L1/L2。核 A 和核 B 都缓存了同一缓存行，A 写其中一个字节，B 手里那一行就过期，硬件必须保证 B 下次读到新值。最经典的协议是 **MESI**：Modified、Exclusive、Shared、Invalid 四种状态。

核 A 想写某行：先让其他所有核把这一行标成 Invalid，自己独占（Modified）。核 B 之后再读或写：发现副本是 Invalid，必须从核 A 把整行拉过来。

关键：**一致性的粒度是缓存行，不是变量**。

---
id: hl-cq-q32-latency-prefault
node: cpp-questions.h-os
type: qa
step: 3
---
## Q
缺页对低延迟系统意味着什么？低延迟系统怎么应对？

## A
- 第一次碰一块新内存要付**缺页代价，微秒级**。
- 对策：
  - 启动时就把要用的内存**预先触碰**（pre-fault）；
  - 用 `mlock` 防止被换出；
  - 用**大页**（huge pages）减少 TLB 未命中。

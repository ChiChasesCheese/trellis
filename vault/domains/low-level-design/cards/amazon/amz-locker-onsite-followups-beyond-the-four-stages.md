---
id: amz-locker-onsite-followups-beyond-the-four-stages
node: amazon.amz-locker-onsite
type: qa
step: 3
tags: [grown]
---
## Q
在快递柜设计里，除了「分配柜格、取件码、过期」，还可能追加哪些需求？各自改哪里、不改哪里？

## A
常见的追加：多个网点、退货（release / return）、并发、持久化表。多网点：新增 `LockerNetwork`，按距离排序后选「装得下且有空位」的网点，单网点类不动，因为选网点和在网点里选柜格是两件互不依赖的事。退货：授权加「用途」字段（取件／投件），分配逻辑不动。并发：一把锁罩住「选柜、占柜、发码」。持久化：柜格与授权各一张表，内存对象不变。

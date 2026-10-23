---
id: hl-c13-aba
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 16
---
## Q
面试问：ABA 问题是什么？怎么解决？
Interview question: What is the ABA problem?

## A
- CAS 看到值 A，期间被改成 B 又改回 A，CAS **成功**，但结构其实已经变了。
- 解决：带**版本号**的指针、hazard pointer、epoch 回收。
- 相关：无锁结构里的悬空指针（节点被另一线程释放）是同类的内存回收难题。

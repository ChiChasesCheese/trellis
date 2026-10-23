---
id: hl-javaq-rubric-red-lines
node: java-questions.rubric
type: qa
step: 3
---
## Q
Java 技术面里有哪些"红线"说法，一说就扣分？

## A
共同的红线：
- 说"Java 比 C++ 快 / 慢"而**不限定场景**。
- 把**预览特性**说成正式。
- 说 `volatile` 能保证**原子递增**。
- 说"GC 慢所以不能用于低延迟"而**不知道 ZGC**。
- 说"`ConcurrentHashMap` 用分段锁"（那是 Java 7，Java 8 起是 CAS + 桶头 `synchronized`）。
- 把**没跑过的命令输出**当真。

正确姿态：限定场景，区分正式与预览，分开"我测过 / 我记得 / 我不确定"。

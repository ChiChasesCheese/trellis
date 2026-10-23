---
id: hl-javaq-f-q25-demo
node: java-questions.f-concurrency
type: qa
step: 2
---
## Q
一个普通 `boolean` 标志位在自旋循环里被另一个线程读取，JIT 编译后会发生什么？用 `-Xint` 又如何？这个现象说明了什么教训？

## A
实测（写入后等 1.5 秒看读线程是否结束）：
- 普通字段：**false**（读线程永远看不到更新）。
- `volatile` 字段：**true**。
- 用 `-Xint`（纯解释）跑普通字段：**true**——反而"碰巧正常"。

教训：**没有同步的代码"能跑"不说明正确，换个 JIT 状态就坏**；这类 bug 很难复现。解释器每次都真的读内存，JIT 编译后把读提到循环外。

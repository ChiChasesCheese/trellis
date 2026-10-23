---
nodes: [java.gc, java.gc-choices, java.garbage-free, java.safepoints, java.tuning]
tags: [drill]
---
# 练习：Java 订单簿的 p99.9 每隔几秒冒一簇尖峰

一个 Java 订单簿服务，每条行情分配约 400 字节（装箱的 `Long` 键、迭代器、字符串拼接的日志），峰值每秒 100 万条，用 G1，年轻代约 1 GB。延迟图上 p99.9 每隔几秒出现一簇几毫秒的尖峰。另一次出问题时，GC 日志显示最长暂停只有 2 ms，应用里的卡顿探测线程（hiccup meter）却记录到约 80 ms 的停顿。

**要你给出的**
- 算 GC 的触发间隔和每小时的停顿次数，解释为什么降低分配速率比调 GC 参数更直接。
- 对第二个症状写出排查步骤，并解释 80 ms 与 2 ms 的差从哪里来。
- 在"零垃圾改造"和"换分代 ZGC"之间做选择：各自的代价是什么，JDK 21 上开关怎么写，怎样验证你真的做到了零分配。
- 给出一份 JVM 启动参数的起点，逐项说明每一项解决什么问题。

**评分要点**
- 交易关心尾部：平均 50 µs、每一万单有一单被卡 100 ms，均值几乎不变；行情包间隔约 10 到 1000 µs，100 ms 里漏掉上千个包，停顿结束时手里的报价已过期；而行情最忙时分配最快，GC 恰好最频繁 ([[hft-java-gc-fear-gc]])
- 回收频率约等于分配速率除以年轻代大小：400 B × 100 万/s = 400 MB/s，1 GB ÷ 400 MB/s = 2.5 s 一次，每小时约 1440 次停顿；稳态分配为 0，年轻代永远填不满，就没有 GC ([[hft-java-gc-alloc-rate]], [[hft-java-garbage-free-goal]])
- 悄悄分配的四处：装箱（改用原始类型 map）、迭代器（改下标 for）、捕获变量的 lambda、字符串拼接（热路径不格式化日志）；逃逸分析不保证生效 ([[hft-java-garbage-free-hidden-alloc]])
- G1 的暂停目标是软目标不是保证，分配快过回收就退化成整堆 Full GC；停顿长短取决于要搬的存活对象量，年轻代回收几毫秒 ([[hft-java-gc-choices-g1]], [[hft-java-gc-stw]], [[hft-java-gc-young-vs-full]])
- 分代 ZGC：JDK 21 写 `-XX:+UseZGC -XX:+ZGenerational`，只写前一个得到旧的非分代版本；代价是吞吐略低、需要额外堆空间（否则 allocation stall）、占 CPU、不用压缩指针；要在自己的负载上用 GC 日志和 JFR 实测 ([[hft-java-gc-choices-gen-zgc]], [[hft-java-gc-choices-zgc-cost]])
- 80 ms 对 2 ms：一次 safepoint 的总停顿 = 到达安全点的时间（TTSP）+ 操作本身；某线程在没有轮询点的长循环或长时间本地调用里，其他线程干等；排查顺序是卡顿探测线程确认全局停顿、对齐 `-Xlog:safepoint` 的到达时间与停顿时间、用 JFR 或线程转储找当时的长循环、最后查操作系统 ([[hft-java-safepoints-ttsp]], [[hft-java-safepoints-diagnose]])
- 除 GC 外的全局停顿：去优化、线程栈转储和堆转储（线上敲一次 `jstack` 或 `jmap` 就停一下）；开 `-Xlog:safepoint` 观察 ([[hft-java-safepoints-hidden-pauses]], [[hft-java-safepoints-observe]])
- 验证零分配：循环前后读 `ThreadMXBean.getThreadAllocatedBytes` 差值应为 0，可以写成单元测试；也可看稳态 `-Xlog:gc` 不再出现年轻代回收、JFR 分配事件、JMH 的 `-prof gc`。参数起点（固定堆、`AlwaysPreTouch`、分代 ZGC、大页、GC 与 safepoint 日志）每项都要实测，一次改一处 ([[hft-java-garbage-free-verify]], [[hft-java-tuning-checklist]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：

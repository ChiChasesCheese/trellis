---
id: hl-javaq-b-q06-follow-ups
node: java-questions.b-versions
type: qa
step: 8
---
## Q
追问：为什么要移除偏向锁？你会把 G1 换成 ZGC 吗？从 Java 8 升级到 21 最主要的摩擦在哪里？
Why was biased locking removed? Would you move from G1 to ZGC?

## A
- **偏向锁为什么移除**：维护成本高、现代并发场景收益小、撤销要进 safepoint（一般认识）。
- **G1 换 ZGC**：看目标——离线批处理看吞吐，G1 或 Parallel 足够；在线低延迟服务选分代 ZGC（JDK 21 需 `-XX:+UseZGC -XX:+ZGenerational`），测试里暂停远低于 1 ms。
- **升级 8 → 21 的主要摩擦**：JDK 内部 API 被强封装，反射代码要加 `--add-opens`；以及被移除的 API。其余（G1、字符串、锁、JIT）基本白捡。

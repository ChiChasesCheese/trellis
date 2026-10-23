---
id: hl-javaq-a-q04-follow-ups
node: java-questions.a-speed
type: qa
step: 18
---
## Q
追问：JVM 为什么不一开始就把所有方法都编译掉？怎么看到哪些方法已经被编译？
Why can't the JVM just compile everything immediately? How would you see which methods are compiled?

## A
- **不全部立即编译**：编译本身很贵（占 CPU 和时间）；而且**没有 profile 就没有优化信息**（不知道类型分布、分支概率）。分层编译（先解释、再 C1、再 C2）就是折中。
- **看编译了哪些方法**：`-XX:+PrintCompilation`，输出里带 `%` 的行是 OSR 编译。
- 查阈值：`-XX:+PrintFlagsFinal`。

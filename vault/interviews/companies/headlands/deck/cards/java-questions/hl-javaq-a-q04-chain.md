---
id: hl-javaq-a-q04-chain
node: java-questions.a-speed
type: qa
step: 16
---
## Q
JVM 启动慢的原因链是什么？阈值怎么查？只调用几次但在长循环里的方法怎么处理（OSR）？

## A
原因链：
1. 字节码被**解释执行**，比编译后慢约一个数量级；每个方法 / 循环有计数器。
2. 计数器过阈值（例如 `Tier4InvocationThreshold=5000`，用 `-XX:+PrintFlagsFinal` 查）→ 入编译队列，由**后台编译线程**编译，完成后才切换。
3. C1 版本带 profiling，稍慢；够热再由 C2 激进编译，可能要几十到几百毫秒。
4. 方法只调用几次但在**长循环**里：用 **OSR**（栈上替换，on-stack replacement）在循环中途切换到编译版本。`-XX:+PrintCompilation` 输出里带 `%` 的行就是 OSR。

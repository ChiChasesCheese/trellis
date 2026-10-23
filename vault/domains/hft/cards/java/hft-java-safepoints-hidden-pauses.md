---
id: hft-java-safepoints-hidden-pauses
node: java.safepoints
type: qa
step: 3
---
## Q
除了 GC，JVM 里还有哪些操作会触发全局停顿？

## A
凡是需要全局一致状态的操作都要进 safepoint，常见的有：
- **去优化**（deoptimization）：编译假设失效时要批量丢弃编译代码；
- **类加载与卸载相关操作**，具体取决于 JVM 版本；
- **偏向锁撤销**：这是历史选项，JDK 15 起默认关闭，JDK 18 起已移除；
- **线程栈转储与堆转储**：`jstack`、`jmap`、`jcmd Thread.print` 等运维命令在线上一敲，整个 JVM 就会停一下；
- 某些 JFR 和调试操作。

所以当 GC 日志看起来很干净、延迟却仍有尖刺时，要去看 safepoint 日志。对交易进程，线上的诊断命令也应该有纪律，不能随手执行。

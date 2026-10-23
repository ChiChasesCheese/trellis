---
id: hl-j19-gc-logs-jfr
node: java21.j19-runtime-zgc-jit
type: qa
step: 11
---
## Q
怎么观察 GC？写出 GC 日志、启动 JFR、运行中开/导出 JFR、读 JFR 事件的命令。JFR 开销多大？

## A
```
-Xlog:gc                        # 每次 GC 一行
-Xlog:gc*:file=gc.log           # 详细，写文件
-XX:StartFlightRecording:filename=rec.jfr,settings=profile
jcmd <pid> JFR.start / JFR.dump ...
jfr print --events jdk.GCPhasePause rec.jfr
```
**JFR**（Java Flight Recorder）是 JVM 内置的事件记录器，开销很低（约 **1%**），可在生产常开。记录 GC 暂停、JIT 编译、线程阻塞、锁竞争、分配热点、`jdk.VirtualThreadPinned` 等。

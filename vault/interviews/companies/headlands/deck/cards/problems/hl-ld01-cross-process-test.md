---
id: hl-ld01-cross-process-test
node: problems.ld01-spsc-channel
type: qa
step: 12
---
## Q
怎么测试跨进程代码、保证不挂死？子进程的 `java` 路径、类路径、预览开关、确定性消息各怎么处理？

## A
1. **找 `java`**：`ProcessHandle.current().info().command()`（`Optional<String>`），取不到退回 `System.getProperty("java.home")/bin/java`；
2. **类路径**：`System.getProperty("java.class.path")` **加上**被测类和子进程入口类所在目录（`getProtectionDomain().getCodeSource().getLocation()`），去重。用 JUnit console 的 `--class-path` 跑时，`java.class.path` 只有 junit 的 jar，被测类在另一个类加载器里，光传 `java.class.path` 子进程 `ClassNotFoundException`；
3. **预览特性**：JDK 21 的 FFM 是预览，子进程要 `--enable-preview`；再加 `-XX:+UseSerialGC`（子 JVM 启动更快、线程更少）；
4. **不挂死**：子进程成功时打印 `OK <count>` 并以 0 退出，失败打印 `FAIL <原因>` 以 1 退出；父进程 `waitFor(超时)`，超时 `destroyForcibly()`（`finally` 里也调，不留孤儿）；两端的自旋循环都带**截止时间**（`System.nanoTime()`，每 1024 圈检查一次）——任何一端挂死都不能让整个测试挂死；**测试不能依赖 `Thread.sleep` 对时序**，协议自己处理（`magic` 最后写）；
5. **抓得到丢 / 重 / 乱序**：每条消息的长度和内容完全由序号决定（splitmix64 小哈希算出长度 8..56，前 8 字节是序号大端，其余由伪随机数派生）；收的一端只靠「我期待第 `seq` 条」校验，丢、重复、乱序、截断 / 损坏都对不上；最后验证「恰好 count 条且 `isDrained`」抓多发；
6. 生产 / 消费写成 `public static` 方法，进程内测试复用，两端对「正确」的定义一致；子进程入口 `switch (mode)` 表达式选 `consume`/`produce`。

三个用例：父生产→子消费；子生产→父消费；父先写完并 `close`，子之后才启动再读（证明数据在文件里）。实测 171 / 151 / 34 ms。

边界：文件不存在 / 太小 / 全零 / 随机内容；`close` 后访问；`close` 后重开仍有积压；子进程崩溃 / 超时不挂死。

测试里的堆 `byte[]` 段会 `Misaligned access`，用 `Arena.ofShared().allocate(bytes, 128)`。

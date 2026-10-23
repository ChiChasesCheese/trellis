---
id: hl-sd03-strategy-interface
node: system-design.sd03-low-latency-trading
type: qa
step: 15
---
## Q
策略接口怎么设计才能保证决定性？写出接口，并说明 `Clock` 和多输入源顺序的处理。

## A
```java
interface Strategy {
    void onBook(int instrument, BookView book, Clock clock, IntentSink out);
    void onExec(ExecView report, Clock clock, IntentSink out);
    void onTimer(long timerId, Clock clock, IntentSink out);   // 由事件流里的 Tick 事件触发
}
```
策略只看到「事件」并输出「意图」，没有 I/O、没有时钟读取、没有线程。
- `Clock` 来自**事件里的时间戳**（硬件时间戳），而不是 `System.nanoTime()`，回放时得到相同的时间，决定性才成立；
- `IntentSink` 写入预分配的意图缓冲，不创建对象；
- **多个输入源的顺序**：分片线程从行情环、回报环、命令环取事件，顺序由线程实际消费顺序决定，是非决定性来源之一。解决：**日志记录的是消费顺序**（线程处理前把每个事件 + 消费序号写进日志环），回放按日志顺序喂入。

决定性杀手：读墙上时钟、`HashMap` 遍历顺序、浮点、无种子 `Random`、依赖线程调度、依赖内存地址（`identityHashCode`）。

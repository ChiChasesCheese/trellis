---
id: hl-os-park-vs-spin
node: foundations.os-processes-threads-ipc
type: qa
step: 11
---
## Q
两个线程来回传一个标志位，`park/unpark` 版和忙等（busy-spin）版往返耗时各是多少？为什么差这么多，代价是什么？

## A
20 万个往返实测：`park/unpark` 往返约 **3099 ns**，忙等往返约 **85 ns**（另一次 2529 / 90 ns，量级一致）。一个往返含两次交接，所以 park/unpark 每次交接约 **1.5 µs**，忙等约 **40 ns**，差约 **36 倍**。

忙等快，是因为两个线程一直占着核、缓存是热的，交接只是一个缓存行在两个核间传一下（几十 ns）；`park` 要睡眠让出 CPU，唤醒时内核把线程放回就绪队列并调度。忙等用 `Thread.onSpinWait()` 提示 CPU。

代价：忙等**烧满一个核**，只在能为每个热线程分配专属核的系统（交易系统）才用。所以 HFT 常见「一个线程一个核，线程里 `while (true) { poll(); }`」。

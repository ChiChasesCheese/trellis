---
id: hl-sd03-architecture
node: system-design.sd03-low-latency-trading
type: qa
step: 8
---
## Q
单台 co-location 主机上的总体架构：各线程负责什么，分片线程依次做哪五步？

## A
- **NIC**：硬件时间戳，kernel bypass，轮询；
- **核 0 Feed Handler**：A/B 仲裁 → 序号检查 / 缺口 → 按品种分发到分片，每分片一条 SPSC 环；
- **核 1..k 分片线程**（独占核心，忙等，run-to-completion）：取一条事件（行情 / 回报 / 命令 / 定时），依次：① 记入「输入日志环」（序号 + 硬件时间戳）；② 解码（flyweight）→ 更新订单簿（数组）；③ 策略 `onBook(...)` → 订单意图（预分配结构）；④ 风控闸门（O(1) 数组查表，不通过 → 拒绝事件也记日志）；⑤ 订单状态机登记 → 编码到发送缓冲 → 交给 Gateway 的 SPSC 环；
- **核 k+1 Order Gateway**（每个场所一条 TCP 会话）：会话序号、心跳、限速、编码 / 发送，回报解码后路由回分片；
- **旁路**（非关键，有损，永不阻塞热线程）：Journaler（日志环 → mmap 追加 → 异步复制）、监控线程（延迟直方图、指标）、控制面（熔断开关、限额、参考价，单写者，热线程只读）；
- **独立进程**：Risk Monitor、Drop-copy 对账器、市场数据落盘（给研究）。

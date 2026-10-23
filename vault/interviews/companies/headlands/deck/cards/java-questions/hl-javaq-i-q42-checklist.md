---
id: hl-javaq-i-q42-checklist
node: java-questions.i-network
type: qa
step: 9
---
## Q
按收益大致排序，降低网络延迟的七项具体措施是什么？

## A
1. **协议与序列化**：定长二进制（`ByteBuffer` / `MemorySegment` + 定义好的偏移，读字段不解析）；避免 `ObjectOutputStream`（慢、占内存、有安全问题）与每条消息分配对象。
2. **写合并**：一条消息一次 `write`；批处理与延迟要权衡；`TCP_NODELAY`。
3. **线程模型**：专用网络线程，**忙轮询**而不是睡眠唤醒（唤醒要几微秒到几十微秒）；绑核、隔离核；GC 不能抢它。
4. **内核层**：调整 socket 缓冲区；中断亲和性（IRQ affinity）；`SO_BUSY_POLL`；关闭节能状态（C-states）。
5. **内核旁路**（Solarflare Onload、DPDK 等）：用户态直接收发包；Java 没有原生一等支持，通常经 JNI / FFM 或厂商库，这是 C++ 更占优的领域。
6. **UDP 多播**：交易所行情常见；无重传，用序号检测丢包、另路补发。
7. **度量**：硬件时间戳、`ss -ti`、抓包；应用内用单调时钟 `System.nanoTime` 测每跳，看分位数。

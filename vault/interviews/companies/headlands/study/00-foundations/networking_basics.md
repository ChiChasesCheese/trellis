# 基础课 · 网络基础：TCP / UDP / 组播、延迟与吞吐、Nagle、内核旁路、Java NIO 与虚拟线程

> 写法说明见 `study/TEXTBOOK.md`。配套代码：[`examples/NetDemo.java`](examples/NetDemo.java)（Nagle 实验、NIO `Selector` 回显服务器 vs 虚拟线程回显服务器、回环接口上的 UDP 组播与丢包检测）。
> **重要说明**：所有实测都在**同一台机器的回环接口**上跑，测的是软件和内核的开销，**不是**网线上的延迟；本机是 macOS，某些 Linux 上的现象在这里不会复现，会在对应小节明说。
> 前置：[os_processes_threads_ipc](os_processes_threads_ipc.md)（系统调用、上下文切换）。
> 被谁引用：目前没有问题讲义直接依赖本章；它直接对应 JD 里的 "networking"。`hc02`/`hc03`/`hc04` 里的虚拟线程小节在第 9 节有网络场景下的展开。
> 运行：`javac --release 21 --enable-preview NetDemo.java && java --enable-preview NetDemo`。

---

## 0. 这一章在讲什么

Headlands 是做高频/低延迟交易的公司。交易系统的一条链路大致是：

```text
交易所 ──(组播行情, UDP)──▶ 行情解码 ──▶ 策略 ──▶ 风控 ──▶ 订单网关 ──(TCP/专有协议)──▶ 交易所
     ◀───────────────────── 往返延迟：微秒级，每一微秒都有人在量 ─────────────────────▶
```

两端都是网络。所以面试时有可能问：TCP 和 UDP 的区别？为什么交易所行情用组播？Nagle 算法是什么，为什么要设 `TCP_NODELAY`？延迟和吞吐有什么区别？什么叫内核旁路？Java 里怎么写网络程序，NIO 和虚拟线程怎么选？

本章从零讲起。顺序：协议栈与套接字 → TCP → UDP → 延迟 vs 吞吐 → Nagle 与延迟确认 → 组播 → 内核旁路 → Java NIO → 虚拟线程。

---

## 1. 协议栈与套接字（socket）

### 1.1 分层

网络通信被拆成若干层，每层只关心自己的事，上层把数据交给下层「打包」：

```text
应用层     你的程序：行情消息、订单消息（FIX、ITCH、自定义二进制）
   ▼ 交给
传输层     TCP 或 UDP：端口号（区分同一台机器上的不同程序）；TCP 还负责可靠性
   ▼ 加上头部
网络层     IP：IP 地址（区分机器）、路由（一个包怎么从 A 到 B）
   ▼ 加上头部
链路层     以太网：MAC 地址、网卡；一帧最多 1500 字节载荷（MTU，通常）
   ▼
物理层     光纤、铜线、无线电
```

每一层给数据加一个"头"。一个以太网帧里承载一个 IPv4 包（头 20 字节），里面是一个 TCP 段（头至少 20 字节）或 UDP 数据报（头 8 字节）：

```text
| 以太网头 14B | IP 头 20B | TCP 头 20B | 应用数据 ≤ 1460B | 以太网尾 4B |
                           └────── 一个 TCP 段：最大段长 MSS = 1500 − 20 − 20 = 1460 ──────┘
```

这就是为什么 UDP 数据报在 IPv4 + 以太网下，不分片的最大载荷是 1500 − 20 − 8 = **1472 字节**（交易所的行情包通常刻意不超过它）。

### 1.2 套接字（socket）

**套接字**是操作系统提供给应用程序的网络通信接口。在 Unix/Linux 里，套接字也是一个**文件描述符**（整数），可以 `read`/`write`/`close`。

TCP 服务端的标准流程（Berkeley sockets API，1983 年起至今未变）：

```text
服务端                                      客户端
socket()    创建套接字
bind()      绑定到 (IP, 端口)
listen()    开始监听，设置等待队列(backlog)
accept()    阻塞等待连接 ◀───────────────  socket(); connect()  发起连接
                    ←──── 三次握手完成 ────▶
read()/write() ◀────────── 数据 ───────────▶ write()/read()
close()                                       close()
```

Java 对应：`ServerSocket`/`Socket`（阻塞）、`ServerSocketChannel`/`SocketChannel`（NIO，第 8 节）。

### 1.3 一个字节从 `write` 到网线：数据的旅程

```text
应用 write(sock, buf)
   │  系统调用 (~几百 ns)
   ▼
内核：把数据拷贝进 socket 发送缓冲区 (SO_SNDBUF)  ← write 在这里就返回了，数据可能还没发出
   ▼
TCP：切成段、加序号、加校验和；决定"现在能不能发"（拥塞窗口、对端接收窗口、Nagle）
   ▼
IP：加 IP 头，查路由表
   ▼
网卡驱动：放进网卡的发送环形队列 (TX ring)，网卡 DMA 取走并发出
```

接收方向反过来：网卡收到帧 → DMA 写进内存的接收环 → 触发中断（或轮询）→ 内核协议栈处理 → 放进 socket 接收缓冲区（SO_RCVBUF）→ 应用 `read` 把它拷贝到用户缓冲区。

**两个后果**：(1) `write` 返回 ≠ 对方收到了，只代表数据进了内核缓冲区；(2) 接收缓冲区满了，TCP 会让对方慢下来，UDP 则**直接丢包**。

---

## 2. TCP

### 2.1 是什么

**TCP**（Transmission Control Protocol，RFC 9293）提供：**面向连接的、可靠的、有序的字节流**。

* **面向连接**：通信前先建立连接（三次握手），结束时关闭。
* **可靠**：每个字节都有序号；接收方确认（ACK）；丢了就重传。
* **有序**：接收方按序号重新排好，应用看到的就是发送顺序。
* **字节流**：**没有消息边界**！发送方 `write` 100 字节两次，接收方可能一次 `read` 到 200 字节，也可能先读到 60 字节再读到 140 字节。

### 2.2 三次握手

```text
客户端                                   服务端
  │ ──── SYN (seq=x) ───────────────────▶ │   "我想连你，我的起始序号是 x"
  │ ◀─── SYN+ACK (seq=y, ack=x+1) ─────── │   "好，我的起始序号是 y，我收到了你的 x"
  │ ──── ACK (ack=y+1) ─────────────────▶ │   "收到"
  │         连接建立，开始传数据            │
```

握手要花 **1 个往返时间（RTT）**才能开始发数据。→ 交易网关会**长期保持连接**，不会为每个订单新建连接。

### 2.3 可靠性是怎么做的

```text
发送方：  [seq=1000 len=100] [seq=1100 len=100] [seq=1200 len=100]
接收方：  收到第 1、3 段，第 2 段丢了
          → 回复 ACK=1100 ("我期待的下一个字节是 1100")
          → 发送方发现 ACK 一直是 1100（收到重复 ACK）或超时 → 重传 seq=1100 那一段
```

* **超时重传**：发送后一段时间（RTO，由 RTT 估计）没收到 ACK 就重发。Linux 的最小 RTO 是 200 ms——一次丢包可能带来 200 ms 的延迟尖刺！
* **快速重传**：连续收到 3 个重复 ACK 就立刻重传，不等超时。

### 2.4 流量控制与拥塞控制

* **流量控制**：接收方在每个 ACK 里告诉对方"我的接收缓冲区还剩多少"（**接收窗口**）。发送方不能发超过它。防止快发慢收。
* **拥塞控制**：网络中间有限的链路。发送方维护**拥塞窗口**（cwnd）：连接刚开始用**慢启动**，窗口每个 RTT 翻倍（初始 10 个段，RFC 6928），直到丢包，然后退让（具体算法如 CUBIC、BBR 各不同）。实际能发的数据量 = min(接收窗口, 拥塞窗口)。

对低延迟的含义：**新连接开头几个 RTT 吞吐很小**（慢启动）；丢包后 cwnd 减半，延迟抖动。

### 2.5 队头阻塞（head-of-line blocking）

TCP 保证有序，所以如果第 2 段丢了，第 3、4、5 段即使已经到了，**应用也读不到**——它们在内核缓冲区里等着第 2 段重传到达。一次丢包让后面所有数据延迟一个 RTT 甚至一个 RTO。这是交易所行情**不用 TCP 而用 UDP 组播**的重要原因之一（第 6 节）：对行情来说，旧消息丢了再等它，不如先处理新的，缺的另外补。

### 2.6 关闭连接与 `TIME_WAIT`

四次挥手（FIN/ACK）。主动关闭的一方会进入 `TIME_WAIT` 状态，保持约 60 秒（Linux），防止延迟到达的旧包被新连接误收。如果一个服务频繁新建/关闭短连接，大量 `TIME_WAIT` 会耗尽端口。→ 再一次：用长连接。

### 2.7 TCP 的成本与优点总结

| 优点 | 代价 |
|---|---|
| 可靠有序，应用不用管重传 | 队头阻塞；丢包时延迟尖刺（RTO 可达 200 ms） |
| 自动流量/拥塞控制 | 慢启动；窗口调整引入抖动 |
| 全世界通用，防火墙友好 | 握手 1 RTT；每条连接有内核状态；不能组播（一对一） |
| 字节流，任意长度 | 没有消息边界，必须自己定帧（长度前缀等） |

---

## 3. UDP

### 3.1 是什么

**UDP**（User Datagram Protocol，RFC 768）只提供最简单的东西：**把一个数据报（datagram）从 A 发到 B 的某个端口，仅此而已**。

* **无连接**：不握手，想发就发。
* **不保证可靠**：可能丢、可能重复、可能乱序。丢了不会重传。
* **保留消息边界**：发送方一次 `send` 一个数据报，接收方一次 `receive` 拿到完整的一个（或者什么都没有）。没有"半个包"。
* **没有流量/拥塞控制**：你想多快发就多快发（也因此可以把对方或网络淹没）。
* 头部只有 8 字节：源端口、目的端口、长度、校验和。

### 3.2 TCP vs UDP 对比

| | TCP | UDP |
|---|---|---|
| 连接 | 面向连接（握手） | 无连接 |
| 可靠性 | 可靠、有序 | 尽力而为，可能丢/乱/重 |
| 单位 | 字节流（无边界） | 数据报（有边界） |
| 头部大小 | ≥ 20 B | 8 B |
| 延迟 | 受重传/队头阻塞/Nagle 影响 | 最小，无额外机制 |
| 一对多 | 不支持 | **支持组播/广播** |
| 适用 | 订单、文件、HTTP | 行情、DNS、音视频、游戏 |

### 3.3 "UDP 不可靠"不等于"UDP 一定丢包"

在内部数据中心网络里，UDP 丢包很少。可靠性要靠**应用层**补：给每个消息编号、接收方检测缺口、缺失时请求重传（第 6 节）。把可靠性放在应用层，应用才能决定**怎么**补（等重传？忽略？用快照覆盖？），这比 TCP 的"一律等"灵活。

### 3.4 UDP 的两个特有风险

1. **接收缓冲区溢出**：应用 `receive` 太慢，内核缓冲区（`SO_RCVBUF`）满了，新到的包被**静默丢弃**。Linux 上 `netstat -su` 里的 `receive buffer errors`（`/proc/net/snmp` 的 `RcvbufErrors`）计数增长就是这个。→ 加大 `SO_RCVBUF`、让接收线程只做最少的事（立刻取走，交给别的线程处理）、绑核。
2. **分片**：载荷 > MTU 的数据报会被 IP 层分片，任何一片丢了整个数据报作废。→ 保持每个数据报 ≤ 1472 字节。

---

## 4. 延迟（latency）与吞吐（throughput）

### 4.1 是什么

* **延迟**：一个东西从 A 到 B 花多久。单位：秒（微秒 µs、纳秒 ns）。
* **吞吐 / 带宽**：单位时间能传多少。单位：比特每秒（Gbps）、消息每秒。

水管比喻：

```text
 ═══════════════════════════════════════════  水管长度 = 延迟（水从一头流到另一头要多久）
 ═══════════════════════════════════════════  水管粗细 = 带宽（每秒能流多少）
 
 一个粗而长的管：吞吐高，延迟也高（比如跨洋光纤）
 一个细而短的管：吞吐低，延迟低（比如同机房内一条普通链路上发一个小包）
```

**它们是不同的东西，优化一个常常伤害另一个。** 批处理（攒一批再发）提高吞吐、拉高延迟；Nagle 算法就是这样一个批处理；交易系统偏向"每条消息立刻发"，宁可吞吐低一点。

### 4.2 一条消息的延迟由哪几部分组成

```text
端到端延迟 = 传播延迟 + 串行化延迟 + 排队延迟 + 处理延迟

传播延迟   信号在介质里走的时间。光在光纤里约 2×10⁸ m/s，即 约 5 µs/公里（单程）
           芝加哥到纽约（约 1200 km）单程至少约 6 ms —— 所以 HFT 公司愿意花巨资架微波链路
           （空气中接近光速 3×10⁸ m/s，比光纤快约 50%）
串行化延迟  把 N 比特推上线路的时间 = 包大小 / 带宽
           1500 字节在 1 Gbps 上：1500×8/10⁹ = 12 µs；在 10 Gbps 上：1.2 µs
排队延迟   在交换机/路由器/操作系统缓冲区里等待的时间（拥塞时增大，最不可预测）
处理延迟   各设备、协议栈、你的程序处理一个包的时间（内核协议栈每包几微秒；用户态协议栈可到几百 ns）
```

Norvig 的时间表里："send 2K bytes over 1Gbps network = 20,000 ns"，就是串行化延迟（2000×8/10⁹ = 16 µs）加一点开销。

### 4.3 带宽时延积（BDP）与 Little 定律

要把一条链路填满，**在途的数据量**至少要等于 **带宽 × 往返时间**（Bandwidth-Delay Product）：

```text
1 Gbps × 10 ms RTT = 10⁹/8 B/s × 0.01 s = 1.25 MB 必须"在飞"
窗口小于 1.25 MB → 发送方发完窗口就得停下等 ACK，链路填不满
```

更一般的 **Little 定律**（L = λ × W）：系统里平均同时存在的请求数 L = 到达率 λ × 每个请求平均停留时间 W。

* 服务每秒 10,000 个请求，每个平均耗时 100 ms → 同时有 10,000 × 0.1 = **1000 个请求在处理中**。
* 如果每个请求占一个线程，就需要 1000 个线程——这是第 9 节虚拟线程存在的原因之一。

### 4.4 为什么交易系统更关心"尾延迟"

平均延迟 5 µs、但 1/1000 的请求要 500 µs，这 0.1% 的"慢请求"往往发生在最关键的时刻（行情剧烈波动时消息最多，处理最慢）。所以用 p99、p99.9、最大值来衡量。测量时要避免 **coordinated omission**（Gil Tene 提出）：压测工具在等待慢请求时没有继续按计划发请求，导致慢请求被低估。

---

## 5. Nagle 算法、延迟确认与 `TCP_NODELAY`

### 5.1 问题：小包太浪费

假设应用连续写 1 字节 100 次。如果每次都立刻发一个 TCP 段，每个段要带 20 字节 TCP 头 + 20 字节 IP 头 + 14 字节以太网头，**1 字节有效数据背着 54+ 字节开销**。网络和 CPU 都被淹没。

### 5.2 Nagle 算法（RFC 896，John Nagle，1984）

规则（简化）：

> 如果连接上有**已发送但未被确认**的数据，那么**小于一个 MSS 的新数据先攒着**，等到 (a) 收到 ACK，或 (b) 攒够了一个 MSS，才发出去。如果没有未确认的数据，立即发。

效果：应用连续写很多小块，第一块立刻发出，其余的攒起来，等第一块的 ACK 回来后合成一个大段一起发。**用一点延迟换大量的包数**。

### 5.3 延迟确认（Delayed ACK，RFC 1122 4.2.3.2）

接收方不是收到每个段都立刻回 ACK，而是**稍等一下**（Linux 最小约 40 ms，RFC 允许最多 500 ms）：看看有没有数据要回（顺便把 ACK 捎带上）、或者再来一个段（两个段合并确认一次）。目的同样是少发小包。

### 5.4 两者撞在一起：写-写-读的 40 ms 停顿

```text
应用：  write(header 4B)     ← 无未确认数据，立即发出
        write(body 40B)      ← 有未确认数据(header)，且小于 MSS：Nagle 把它扣住，等 header 的 ACK
        read(...)            ← 等对方的回复

服务端：收到 header，但它还在等 body 才能处理；
        延迟确认：先不回 ACK，等 40 ms 看看有没有数据可捎带

客户端 Nagle 在等 ACK ←──→ 服务端 延迟确认 在等数据/计时器
        └───────────── 互相等 40 ms，直到服务端的延迟确认计时器到期 ─────────────┘
```

结果：每个请求/响应多出 **约 40 ms**（Linux）。对交易系统是灾难。

这是 Stuart Cheshire 的著名文章 "TCP Performance problems caused by interaction between Nagle's Algorithm and Delayed ACK" 讨论的现象。

### 5.5 解决

1. **`TCP_NODELAY`**：关闭 Nagle，写下去就立刻发。**低延迟交易系统几乎总是设置它**。
2. **一次写完**：把 header 和 body 拼进同一个缓冲区一次 `write`，或者用聚集写（`GatheringByteChannel.write(ByteBuffer[])` / `writev`）。这是更根本的做法——避免产生"写-写-读"模式。
3. `TCP_QUICKACK`（Linux）：关闭延迟确认（但需要每次 `read` 后重新设置）。

Java 里：

```java
import java.net.Socket;
import java.net.StandardSocketOptions;
import java.nio.channels.SocketChannel;

public class NoDelay {
    static void configure(Socket s) throws Exception {
        s.setTcpNoDelay(true);                      // 传统 API
    }

    static void configure(SocketChannel ch) throws Exception {
        ch.setOption(StandardSocketOptions.TCP_NODELAY, true);   // NIO API
        ch.setOption(StandardSocketOptions.SO_RCVBUF, 1 << 20);  // 接收缓冲区 1 MB（实际值由内核决定/封顶）
    }
}
```

### 5.6 本机实测

`NetDemo` 第 1 部分：客户端每个请求先写 4 字节 header，再写 40 字节 body，然后等 44 字节回显（"写-写-读"）。

```text
TCP_NODELAY=false :        121 us per request/reply
TCP_NODELAY=true  :         78 us per request/reply
(On Linux the first line is typically ~40,000 us: Nagle waits for an ACK, the peer delays its ACK. macOS loopback does not reproduce it.)
```

**诚实说明**：这一现象在本机（macOS 回环）**没有复现**：两行都是百微秒量级，没有 40 ms 的停顿；`NODELAY` 略快（这次 78 对 121 µs；另几次运行是 85 对 148、119 对 109，方向不稳定），差别在噪声范围内。macOS 的 TCP 栈对回环的延迟确认处理和 Linux 不同。"Linux 上典型约 40 ms"这句话来自文献（Stevens《TCP/IP Illustrated》；Cheshire 的文章），我**没有在 Linux 上亲自验证**。面试时可以说"这是经典现象，在 Linux 上是 40 ms 量级"，但不要说成"我测过"。

**Nagle 本来是为了什么**——`NetDemo` 第 1b 部分：对一个只负责读取的服务端，**连续写 20 万次 1 字节**：

```text
TCP_NODELAY=false :     92 ms
TCP_NODELAY=true  :    341 ms
```

开着 Nagle（`NODELAY=false`）**快 3.7 倍**（另几次运行是 88 对 495 ms 即 5.6 倍，波动较大，方向稳定）：Nagle 把许多个 1 字节合并成大段，发出的包少得多；关掉之后每次 `write` 几乎都变成一个独立的小包。这说明 Nagle 不是"坏东西"，它对"批量写小块"的吞吐是有益的；问题只出在**请求/响应的交互式小消息**上。

---

## 6. 组播（multicast）：交易所怎么把行情发给几百个客户

### 6.1 问题

交易所每秒产生几十万条行情更新（每个买卖盘变化一条），所有订阅的客户（几百家公司）都要收到，**同一时刻、同样顺序**。

* **用 TCP 一对一发给每个客户**：交易所要维护几百条连接，同一条消息复制几百遍发出去；发给不同客户的时间有先后——**不公平**（先发的客户先收到）；一个慢客户的缓冲区满了还会拖住发送线程。
* **组播**：交易所只发**一份**数据到一个**组地址**，网络设备（交换机/路由器）在需要分叉的地方复制它，每个订阅者各收到一份。

```text
                    ┌──▶ 客户 A
交易所 ──1 份──▶ 交换机 ──▶ 客户 B           发送方只发一次，交换机在端口处复制
                    ├──▶ 客户 C           复制发生在硬件里，各客户几乎同时收到
                    └──▶ （未订阅的端口收不到）
```

对比：

| | 单播 unicast | 广播 broadcast | 组播 multicast |
|---|---|---|---|
| 目的 | 一个接收者 | 子网里所有人 | 订阅了这个组的人 |
| 发送方发几次 | 每个接收者一次 | 一次 | **一次** |
| 适合 | 订单 | 局域网发现 | **行情分发** |

### 6.2 它怎么工作

* **组地址**：IPv4 的 `224.0.0.0/4`（224.x.x.x – 239.x.x.x）。`239.0.0.0/8` 是"本地管理"范围，私有网络里随便用。
* **加入组**：接收方用 **IGMP**（Internet Group Management Protocol）告诉本地交换机/路由器"我想收这个组"。交换机用 **IGMP snooping** 只把这个组的流量转发到有订阅者的端口。
* **TTL**：组播包的 TTL 控制它能跨几跳路由器；TTL = 1 表示只在本网段。
* **UDP**：组播只能用 UDP（TCP 是一对一的）。

### 6.3 UDP 不可靠，行情怎么保证不丢？—— 序号 + 缺口检测 + 冗余

真实的交易所协议（以 Nasdaq TotalView-ITCH over MoldUDP64、CME MDP 3.0 为例，细节见各自的公开规范）都用同一套思想：

1. **每个消息（或每个包）带一个单调递增的序号**。
2. **接收方检测缺口**：收到序号 1000，下一个应该是 1001；收到 1003 就知道 1001、1002 丢了。
3. **补救**：
   * 通过一个单独的**重传/回补通道**（常常是 TCP 或另一组 UDP）请求缺失的序号范围；
   * 或者用一个定期发布的**快照**通道，让落后太多的接收方直接从最新快照重建订单簿（这是为什么订单簿重建是 hc05 的主题之一）。
4. **A/B 双线冗余**：同一份行情在两条独立的网络路径（A 线、B 线）上各发一份；接收方对两条线的数据**按序号去重、取先到的**。一条线丢包，另一条线大概率还有。

### 6.4 本机实测：回环上的组播与缺口检测

`NetDemo` 第 3 部分：一个发送者往 `239.255.42.99:45678` 发送 10000 个带序号的数据报，**故意每 500 个丢掉一个**（序号 499, 999, …, 9999，共 20 个，不发送），两个接收者加入同一个组，各自检测缺口：

```text
receiver 0: got 9980 packets, detected 19 missing sequence numbers (20 were dropped; the last one, seq 9999, is invisible: no later packet reveals the gap)
receiver 1: got 9980 packets, detected 19 missing sequence numbers (20 were dropped; the last one, seq 9999, is invisible: no later packet reveals the gap)
```

注意两件事：

1. **一次发送，两个接收者各收到一份**——组播起作用了。每个接收者收到 9980 个包（10000 减去故意不发的 20 个）。
2. **检测到 19 个缺口，不是 20 个**：最后一个丢失的序号 9999 之后再没有包到达，接收方没有"更大序号"可以对比，**无法发现**末尾的丢失。这是真实的设计问题：解决办法是发送方定期发**心跳**（heartbeat）消息，携带当前最新序号，让接收方即使没有数据也能发现自己落后了。

（演示代码的一个细节：接收端是非阻塞的，包可能还在路上，所以发送完最后一个包后要睡 100 ms 再做最后一次排空。我第一次写时漏了这步，只收到 9979 个包，看起来像"多丢了一个"，其实是最后一个包还没到——这种"测量方式本身造成的假象"在网络实验里很常见。）

### 6.5 Java 里加入组播组

```java
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.StandardProtocolFamily;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.DatagramChannel;
import java.nio.channels.MembershipKey;

public class MulticastReceiver {
    public static void main(String[] args) throws Exception {
        InetAddress group = InetAddress.getByName("239.255.42.99");
        NetworkInterface ni = NetworkInterface.getByName("lo0");       // Linux 上通常是 "lo"，或具体网卡如 "eth0"
        if (ni == null) { System.out.println("interface not found"); return; }
        try (DatagramChannel ch = DatagramChannel.open(StandardProtocolFamily.INET)) {
            ch.setOption(StandardSocketOptions.SO_REUSEADDR, true);     // 多个接收者可共用端口
            ch.bind(new InetSocketAddress(45678));
            MembershipKey key = ch.join(group, ni);                     // 发 IGMP 加入报文
            ch.configureBlocking(false);                                // 非阻塞：receive 没数据时返回 null
            ByteBuffer buf = ByteBuffer.allocateDirect(2048);           // 直接缓冲区：避免多一次拷贝
            long deadline = System.nanoTime() + 200_000_000L;
            while (System.nanoTime() < deadline) {                      // 忙轮询（busy poll）：低延迟接收的典型写法
                buf.clear();
                if (ch.receive(buf) == null) continue;
                buf.flip();
                System.out.println("got " + buf.remaining() + " bytes");
            }
            key.drop();                                                  // 离开组
        }
    }
}
```

要点：

* `DatagramChannel` + `join` 是 NIO 的组播 API（传统的 `MulticastSocket` 也能用）。
* **选对网卡**：`ni` 必须是实际收组播的那个接口；多网卡机器上选错了会"收不到"，是常见故障。
* 真实的行情接收器：非阻塞 + 忙轮询 + 预分配的直接缓冲区 + 绑核；包到达后**立刻**取走，交给下游，绝不在接收线程里做重活（否则 `SO_RCVBUF` 溢出丢包，3.4 节）。

---

## 7. 内核旁路（kernel bypass）——一段话版

标准路径下，一个包从网卡到你的程序要经历：网卡中断（或轮询）→ 内核协议栈处理 → 放入 socket 缓冲区 → 你调用 `read`/`recv`（系统调用）→ 内核把数据拷贝到你的缓冲区；每步都是微秒量级的开销加上一次内核/用户态切换和一次拷贝。**内核旁路**的思路是让用户态程序**直接**操作网卡：把网卡的收发环形队列直接映射到用户态内存，程序**轮询**这些队列，在用户态自己解析协议，**不经过内核、没有系统调用、没有中断、没有拷贝**，把每包的处理时间从几微秒降到几百纳秒甚至更低。代表技术：**DPDK**（Intel 起头的开源用户态网卡驱动框架）、**Solarflare / AMD 的 OpenOnload 与 `ef_vi`**（Onload 通过 `LD_PRELOAD` 拦截 socket 调用，让普通的 socket 程序不改代码就跑在用户态协议栈上）、**NVIDIA（原 Mellanox）的 VMA**、Linux 的 **AF_XDP** 和 **io_uring**（后者不是旁路，是减少系统调用）。**代价**：要独占 CPU 核心做 100% 忙轮询、要特定的网卡、失去 `tcpdump`/`iptables` 等常规工具、运维复杂。Java 程序接入的方式：通过 JNI/FFM 调用 C 库，或使用 Onload 这种对 socket API 透明的方案（Java 的 `Socket`/`DatagramChannel` 不改代码就受益）。更极端的做法是把解码逻辑放进网卡上的 **FPGA**。面试里答出"为什么要旁路（内核栈的中断、系统调用、拷贝开销）、怎么做（用户态轮询网卡队列）、代价是什么"就足够了。

---

## 8. Java NIO 基础：`SocketChannel`、`Selector`、`ByteBuffer`

### 8.1 阻塞 I/O 的问题

传统 `Socket.getInputStream().read(...)` 是**阻塞**的：调用后线程睡眠，直到有数据。要同时服务 N 个连接，要么 N 个线程（每个线程 1 MB 栈、上下文切换），要么……

**C10K 问题**（Dan Kegel，1999）：怎么在一台机器上处理 1 万个并发连接？答案是**I/O 多路复用**：一个线程同时监视很多个套接字，哪个有数据就处理哪个。

### 8.2 `Selector`：问内核"哪些套接字准备好了"

`Selector` 封装了操作系统的多路复用机制：Linux 的 **epoll**、macOS/BSD 的 **kqueue**（更老的 `select`/`poll`）。

```text
一个线程：
    while (true) {
        selector.select();                       // 睡眠，直到至少一个注册的通道"就绪"
        for (每个就绪的 key) {
            if 可接受(accept)  → 接受新连接，设为非阻塞，注册到 selector 的"可读"事件
            if 可读(read)      → 读数据（不会阻塞，因为已经就绪）
            if 可写(write)     → 写剩余数据
        }
    }
```

核心概念：

* **非阻塞模式**：`configureBlocking(false)`，`read` 没数据就立即返回 0，`write` 缓冲区满就写一部分（或 0）。
* **SelectionKey**：通道在 selector 上的注册；`interestOps` 是你关心的事件（`OP_ACCEPT`、`OP_READ`、`OP_WRITE`、`OP_CONNECT`）。
* **就绪不等于完成**：可读只表示"此刻读不会阻塞"，不表示"一个完整消息到了"（TCP 是字节流，第 8.4 节）。

### 8.3 `ByteBuffer`：NIO 的缓冲区，三个游标

`ByteBuffer` 是 NIO 读写的载体，有三个数：**position**（下一个读/写位置）、**limit**（可操作区域的末端）、**capacity**（总容量）。

```text
刚创建 allocate(8):             [ _ _ _ _ _ _ _ _ ]      position=0  limit=8  capacity=8
                                  ↑p                  ↑l

channel.read(buf) 读入 5 字节:   [ a b c d e _ _ _ ]      position=5  limit=8
                                              ↑p      ↑l

buf.flip() (写模式→读模式):      [ a b c d e _ _ _ ]      position=0  limit=5
                                  ↑p          ↑l          现在可以从 0 读到 5

读走 3 个字节(get×3):            [ a b c d e _ _ _ ]      position=3  limit=5
                                        ↑p    ↑l          还剩 2 个字节没处理（不完整的消息）

buf.compact():                  [ d e _ _ _ _ _ _ ]      position=2  limit=8
                                      ↑p                  把剩余 2 字节挪到开头，切换回"继续写入"模式
```

* `flip()`：写完准备读（limit = position; position = 0）。
* `clear()`：读完准备重新写，丢弃一切。
* `compact()`：读了一部分，保留未读部分，准备继续写入。**处理半包的标准工具**。
* **直接缓冲区**（`allocateDirect`）分配在 JVM 堆外，I/O 时不用多拷贝一次，但分配和释放更贵——应该分配一次、长期复用。

### 8.4 TCP 是字节流：必须自己做"帧"

`read` 一次可能拿到：半个消息、一个整消息、一个半消息、三个消息。所以要在协议里定义**帧边界**，最常见：**长度前缀**（先 4 字节长度，再 N 字节内容）。

```java
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;

public class LengthPrefixed {
    /** 从缓冲区（读模式）里尽可能多地取出完整消息；剩下的半包留在缓冲区。调用前要 flip，调用后要 compact。 */
    static List<byte[]> decode(ByteBuffer buf) {
        List<byte[]> out = new ArrayList<>();
        while (buf.remaining() >= 4) {
            buf.mark();
            int len = buf.getInt();                  // 先看长度
            if (buf.remaining() < len) {             // 内容还没收全
                buf.reset();                          // 回退到长度字段之前，等更多数据
                break;
            }
            byte[] msg = new byte[len];
            buf.get(msg);
            out.add(msg);
        }
        return out;
    }

    public static void main(String[] args) {
        ByteBuffer b = ByteBuffer.allocate(64);
        b.putInt(3).put(new byte[]{1, 2, 3}).putInt(5).put(new byte[]{9, 9});   // 第二条只到了 2/5
        b.flip();
        System.out.println(decode(b).size() + " complete message(s), " + b.remaining() + " byte(s) left over");   // 1 ... 6
        b.compact();                                  // 半包留着，等下次 read 追加
    }
}
```

### 8.5 一个完整的 `Selector` 回显服务器

下面是 `NetDemo.startSelectorEcho` 的精简版（可编译）：

```java
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.StandardSocketOptions;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

public class SelectorEcho {
    public static void main(String[] args) throws IOException {
        ServerSocketChannel server = ServerSocketChannel.open();
        server.bind(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 1024);   // backlog 1024
        server.configureBlocking(false);
        Selector selector = Selector.open();
        server.register(selector, SelectionKey.OP_ACCEPT);
        System.out.println("listening on " + server.getLocalAddress());

        ByteBuffer buf = ByteBuffer.allocateDirect(4096);
        long end = System.nanoTime() + 100_000_000L;           // 演示：只跑 0.1 秒
        while (System.nanoTime() < end) {
            selector.select(10);                                // 最多睡 10 ms；selectNow() 是不睡的忙轮询版本
            Iterator<SelectionKey> it = selector.selectedKeys().iterator();
            while (it.hasNext()) {
                SelectionKey key = it.next();
                it.remove();                                    // 必须手动移除，否则下次还会出现
                if (key.isAcceptable()) {
                    SocketChannel c = server.accept();
                    if (c == null) continue;
                    c.configureBlocking(false);
                    c.setOption(StandardSocketOptions.TCP_NODELAY, true);
                    c.register(selector, SelectionKey.OP_READ);
                } else if (key.isReadable()) {
                    SocketChannel c = (SocketChannel) key.channel();
                    buf.clear();
                    int n = c.read(buf);
                    if (n < 0) { key.cancel(); c.close(); continue; }   // 对端关闭
                    buf.flip();
                    while (buf.hasRemaining()) c.write(buf);    // 简化：假设发送缓冲区有空间（真实代码要处理 OP_WRITE）
                }
            }
        }
        server.close();
        selector.close();
    }
}
```

**真实代码还要处理的**：

* **背压与 `OP_WRITE`**：`write` 可能一次写不完（发送缓冲区满）。这时要把剩余数据保存起来，注册 `OP_WRITE`，等通道可写时继续，写完取消 `OP_WRITE`（否则 selector 会一直忙转）。
* **半包**（8.4）。
* **异常、连接关闭、超时**。
* 这就是为什么实际项目用 **Netty**（成熟的 NIO 框架）或 **Aeron**，而不是手写 `Selector` 循环。

### 8.6 低延迟交易系统里的 `Selector` 用法

* `select()` 会让线程**睡眠**，被唤醒要经过内核调度（os 章：往返约 1.5 µs/次）。低延迟系统用 **`selectNow()` 忙轮询**（不睡眠，立即返回就绪集合）并把线程绑在隔离的核上，以延迟换 CPU。
* `selectedKeys()` 默认会分配迭代器和集合对象，产生垃圾；Netty 用反射把它换成数组实现。
* 用 `allocateDirect` 并复用；避免每个消息 `new byte[]`。

---

## 9. 虚拟线程 + 阻塞式套接字 vs NIO `Selector`

### 9.1 问题：NIO 很快但难写

`Selector` 把一个连接的处理拆成一堆回调式的小片段（半包、背压、状态机），代码难读难调试。阻塞式代码——"读、处理、写"一行接一行——才是人类容易写对的方式，但传统上一个连接一个线程撑不住几万连接。

### 9.2 虚拟线程（JDK 21，JEP 444）怎么解决

**虚拟线程**是由 JVM 调度的轻量级线程，创建几乎免费，可以同时有几十万个。关键机制：

* 虚拟线程运行在少量**载体线程**（carrier，平台线程，默认数量 = CPU 核数）上。
* 当虚拟线程调用**阻塞的套接字 I/O**（`Socket.read`、`ServerSocket.accept`）时，JDK 内部实际用非阻塞 I/O + 一个 poller（epoll/kqueue），把这个虚拟线程**挂起**（unmount，把它的栈保存在堆里），**释放载体线程**去跑别的虚拟线程；数据就绪时再恢复它。
* 对程序员来说：**写的是普通的阻塞代码，得到的是接近 NIO 的扩展性**。

```java
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class VirtualThreadEcho {
    public static void main(String[] args) throws IOException {
        try (ServerSocket server = new ServerSocket(0, 1024, InetAddress.getLoopbackAddress());
             ExecutorService pool = Executors.newVirtualThreadPerTaskExecutor()) {
            System.out.println("listening on " + server.getLocalPort());
            server.setSoTimeout(100);                           // 演示：0.1 秒后退出
            try {
                while (true) {
                    Socket s = server.accept();                 // 阻塞，但只阻塞这个（虚拟）线程
                    pool.submit(() -> {                          // 每个连接一个虚拟线程：thread-per-connection
                        try (s; InputStream in = s.getInputStream(); OutputStream out = s.getOutputStream()) {
                            byte[] b = new byte[4096];
                            int n;
                            while ((n = in.read(b)) > 0) out.write(b, 0, n);   // 直白的阻塞代码
                        } catch (IOException e) { /* 连接关闭 */ }
                        return null;
                    });
                }
            } catch (java.net.SocketTimeoutException done) { /* 演示结束 */ }
        }
    }
}
```

### 9.3 本机实测：两种服务器的对比

`NetDemo` 第 2 部分：100 个并发连接，每个连接做 500 次"发 32 字节、收 32 字节"的乒乓（共 5 万个往返）；客户端是 100 个虚拟线程；对比 NIO `Selector` 单线程回显服务器和虚拟线程回显服务器：

```text
run 0: selector server    286 ms | virtual-thread server    333 ms
run 1: selector server    256 ms | virtual-thread server    341 ms
run 2: selector server    246 ms | virtual-thread server    325 ms
```

* 两者量级一样；虚拟线程版**慢约 15–35%**（这次是 325–341 ms 对 246–286 ms；另一次完整运行是 404–428 对 364–403 ms，慢 7–10%），在这个规模下是同一个量级。
* 这说明：对"大量连接、每个连接大部分时间在等"的 I/O 密集场景，**虚拟线程能用简单的阻塞代码达到接近手写 NIO 的性能**。
* 注意这是回环上的小测试，100 个连接远不到压垮线程模型的程度；真正的差别在连接数到几万、几十万时才出现（虚拟线程 vs 平台线程）。我没有测那个规模，请不要把这个表当成容量结论。

### 9.4 怎么选

| 场景 | 选择 | 原因 |
|---|---|---|
| 业务服务：很多连接，每个请求做点业务逻辑，延迟要求毫秒级 | **虚拟线程 + 阻塞 I/O** | 代码最简单，易调试，扩展性够 |
| 超低延迟（微秒级、确定性）：行情接收、订单网关 | **单线程 + 非阻塞 + 忙轮询（`selectNow`/`receive`）+ 绑核** | 没有调度延迟，没有唤醒抖动，完全可控的内存分配；不让出 CPU |
| 需要精确控制线程-核心绑定 | 平台线程 + 亲和性 | 虚拟线程由 JVM 调度，不能绑核，调度延迟有抖动 |
| 需要成熟的协议编解码、背压、SSL | **Netty** | 现成的事件循环（基于 `Selector`/epoll） |
| CPU 密集计算 | 平台线程池（`ForkJoinPool`） | 虚拟线程对 CPU 密集没有好处（hc03 步骤 8） |

**虚拟线程的坑**（JDK 21）：

1. **固定（pinning）**：在 `synchronized` 块里或本地方法栈上做阻塞操作，虚拟线程无法卸载，**占着载体线程不放**。大量固定会耗尽载体（默认只有 CPU 核数个）。→ 用 `ReentrantLock` 代替 `synchronized` 包裹阻塞调用。（后续 JDK 版本在改善这个问题，但 21 里要小心。）
2. **ThreadLocal**：百万个虚拟线程各自带 `ThreadLocal` 会耗内存；`ScopedValue`（预览）是替代。
3. **不是更快，是更多**：虚拟线程提高的是并发度（同时能挂起的任务数），**不降低单个请求的延迟**。
4. **调度抖动**：虚拟线程被 JVM 的 `ForkJoinPool` 调度，时序不是确定的——对微秒级延迟不适用。

---

## 10. 常见误区

1. **「`write` 返回了，对方就收到了」。**只是进了内核发送缓冲区（第 1.3 节）。
2. **「TCP 保证消息送达，所以不用处理半包」。**TCP 保证字节有序，**不保证**消息边界（第 2.1 节、8.4 节）。
3. **「UDP 一定丢包，所以不可靠不能用」。**数据中心内丢包很少，而且应用层的序号 + 缺口检测比 TCP 的一刀切更灵活（第 6.3 节）。
4. **「设了 `TCP_NODELAY` 就一定低延迟」。**它只消除了 Nagle 的延迟；还有延迟确认、拥塞窗口、系统调用、上下文切换、GC 暂停、锁争用。
5. **「`Selector` 的 `select()` 返回就是消息完整了」。**只是"此刻读不阻塞"。
6. **「虚拟线程让 Java 变快了」。**提高的是并发度，不是单请求延迟；CPU 密集更没用（第 9.4 节）。
7. **用 `localhost` 回环的数字推测网线上的延迟。**回环不经过网卡、不经过交换机、没有传播延迟。本章的数字只代表软件栈的开销。
8. **组播收不到：忘了选网卡 / 防火墙 / IGMP snooping 没配 / `SO_REUSEADDR` / TTL。**组播排障先查这几项。

---

## 11. 面试追问预演

**Q1：TCP 和 UDP 的区别？交易所行情为什么用 UDP 组播？**
答：「TCP 是可靠有序的字节流，有连接、重传、拥塞控制；UDP 是无连接的数据报，不保证可靠。行情要同时发给几百个客户：组播发送一份，由交换机复制，公平且高效；TCP 做不到一对多，也有队头阻塞——丢一个包会卡住后面所有已到的包，行情宁愿用新数据。可靠性由应用层补：消息带序号，接收方检测缺口，通过回补通道或快照恢复，还常用 A/B 双线冗余。」

**Q2：什么是 Nagle？为什么要 `TCP_NODELAY`？**
答：「Nagle 把小写入攒起来，直到前面数据被确认或攒满一个 MSS，减少小包。它和接收方的延迟确认（Linux 约 40 ms）叠加，在写-写-读的模式下会造成每个请求多 40 ms。交易系统发订单是延迟敏感的小消息，所以设 `TCP_NODELAY`。更根本的做法是一次写完整个消息，避免写-写-读。我实测过 Nagle 的本意：20 万次 1 字节写，开着 Nagle 反而快 4–5 倍。」

**Q3：延迟和吞吐的区别？**
答：「延迟是单个消息从发出到收到的时间，吞吐是单位时间能传多少。水管比喻：长度是延迟，粗细是带宽。它们会互相牺牲：批处理提高吞吐、增加延迟。交易系统更关心尾延迟（p99、p99.9），不是平均。」

**Q4：什么是内核旁路？**
答：「标准路径要经过中断、内核协议栈、系统调用和拷贝，每包几微秒。内核旁路让用户态程序直接轮询网卡队列，自己处理协议，不经内核，把每包处理降到几百纳秒。例子是 DPDK、Solarflare 的 Onload。代价是独占核心忙轮询、特定网卡、失去常规网络工具。」

**Q5：Java 里怎么写高并发网络服务？NIO 和虚拟线程怎么选？**
答：「`Selector` 多路复用，一个线程监视很多通道，用非阻塞 I/O；缺点是代码复杂，要自己处理半包和背压，实际用 Netty。JDK 21 的虚拟线程让我写直白的阻塞代码，遇到阻塞 I/O 自动让出载体线程，扩展性接近 NIO；我在回环上测 100 连接，两者同一量级，虚拟线程版慢一成到三成。业务服务我选虚拟线程；微秒级低延迟路径选单线程非阻塞忙轮询加绑核，因为虚拟线程由 JVM 调度，不能绑核，调度有抖动。」

**Q6：TCP 连接断开后怎么知道？**
答：「`read` 返回 -1（对端正常关闭，发了 FIN）或抛 `IOException`（RST/超时）。但如果对端机器直接断电，没有任何包，本端要靠应用层心跳或 TCP keepalive（默认两小时）才能发现，所以交易网关都有应用层心跳。」

---

## 12. 自测题

**Q1（计算）** 一个 TCP 连接的往返时间是 20 ms，带宽 100 Mbps。要充分利用链路，窗口至少多大？

<details><summary>答案</summary>

BDP = 带宽 × RTT = 100×10⁶ bit/s ÷ 8 × 0.02 s = 12.5 MB/s × 0.02 s = 250 KB。窗口小于 250 KB 时发送方会停下来等 ACK，链路填不满。

</details>

**Q2（计算）** 一个 1500 字节的包在 10 Gbps 链路上，串行化延迟是多少？在 1 Gbps 上呢？

<details><summary>答案</summary>

1500 × 8 = 12000 bit。10 Gbps：12000 / 10¹⁰ = 1.2 µs。1 Gbps：12 µs。

</details>

**Q3（Little 定律）** 一个服务每秒 5000 个请求，平均每个请求耗时 200 ms。同时有多少个请求在处理？如果每个请求占一个平台线程，需要多少线程？

<details><summary>答案</summary>

L = λ × W = 5000 × 0.2 = 1000。需要约 1000 个线程（平台线程 1000 个已经比较重，虚拟线程则轻松）。

</details>

**Q4（读代码）** 下面的服务端读取 4 字节长度加内容，哪里有 bug？

```java
import java.io.*;

public class Bug {
    static byte[] readMessage(InputStream in) throws IOException {
        byte[] lenBuf = new byte[4];
        in.read(lenBuf);                                   // (1)
        int len = java.nio.ByteBuffer.wrap(lenBuf).getInt();
        byte[] body = new byte[len];
        in.read(body);                                     // (2)
        return body;
    }
}
```

<details><summary>答案</summary>

两处 `read` 都假设一次读满：`InputStream.read(byte[])` 只保证读到**至少 1 个字节**（或 -1），可能只返回部分数据（TCP 字节流没有边界）。要循环读到足够字节，或使用 `DataInputStream.readFully`。另外 (1) 没检查 -1（连接关闭），`len` 没做上限校验（恶意对端发一个 2 GB 的长度让你 OOM）。

</details>

**Q5（辨析）** 判断：「设置了 `TCP_NODELAY`，把 header 和 body 分两次 `write` 也没问题。」

<details><summary>答案</summary>

不完全对。没有 Nagle 的 40 ms 停顿，但两次 `write` 变成两个小 TCP 段，两次系统调用，对端可能要处理半包。更好的做法是合并到一个缓冲区一次写（或 `writev` 聚集写）：少一次系统调用、少一个包。

</details>

**Q6（设计）** 你要写一个行情接收器：从一个组播组接收 UDP 包，每个包头有 8 字节序号，处理必须按序号递增。收到乱序/缺口怎么办？

<details><summary>答案</summary>

维护 `expectedSeq`。收到 `seq == expected`：处理并 `expected++`，然后检查缓冲里有没有 `expected` 开头的后续包。收到 `seq > expected`：存缺口 [expected, seq)；把这个包暂存（小的重排窗口，几毫秒）；等待 A/B 另一条线的同序号包；窗口超时仍缺则向回补通道请求重传，或等快照。`seq < expected`：重复包（A/B 线的另一份），丢弃。定期心跳携带最新序号以发现末尾丢失（第 6.4 节）。接收线程里只做收包、排序，不做重活，防止 `SO_RCVBUF` 溢出。

</details>

**Q7（概念）** 虚拟线程在 `synchronized` 块里做阻塞的 `socket.read()` 会发生什么？

<details><summary>答案</summary>

在 JDK 21 里会**固定（pin）**载体线程：虚拟线程无法卸载，载体线程被它占着一起阻塞。载体线程默认只有 CPU 核数个，大量这样的虚拟线程会耗尽载体，让所有虚拟线程饥饿。解决：用 `ReentrantLock` 代替 `synchronized`，或避免在持锁时做阻塞 I/O。

</details>

---

## 13. 延伸阅读（只列权威来源）

* **RFC 9293: Transmission Control Protocol (TCP)**（2022，取代 RFC 793）；**RFC 768: UDP**；**RFC 1112: Host Extensions for IP Multicasting**（IGMP 与组播基础）；**RFC 896: Congestion Control in IP/TCP Internetworks**（Nagle，1984）；**RFC 1122: Requirements for Internet Hosts** 第 4.2.3.2 节（延迟确认）与 4.2.3.4 节（Nagle）；**RFC 6928**（初始拥塞窗口 10）。
* **W. Richard Stevens,《TCP/IP Illustrated, Volume 1》（第 2 版 Fall & Stevens）**：TCP 数据流、延迟确认与 Nagle（"TCP Data Flow and Window Management"一章）、拥塞控制。
* **Stuart Cheshire, "TCP Performance problems caused by interaction between Nagle's Algorithm and Delayed ACK"**（stuartcheshire.org/papers/NagleDelayedAck）；**Mogul & Minshall, "Rethinking the TCP Nagle Algorithm", ACM CCR 2001**。
* **Michael Kerrisk,《The Linux Programming Interface》**：第 56–61 章（套接字、TCP/IP 基础、互联网域套接字、高级主题含 `TCP_NODELAY`）、**第 63 章「Alternative I/O Models」**（`select`/`poll`/`epoll`）。
* **W. Richard Stevens,《UNIX Network Programming Vol. 1》**：套接字 API 的经典。
* **Brendan Gregg,《Systems Performance》第 2 版第 10 章「Network」**：网络延迟的各个组成、排队、`ss`/`nstat`/`tcpdump`/`perf` 的用法。
* **Dan Kegel, "The C10K problem"**（kegel.com/c10k.html）：I/O 多路复用的历史动机。
* **Java SE 21 API：`java.nio.channels.SocketChannel`/`Selector`/`DatagramChannel`/`MulticastChannel`、`java.nio.ByteBuffer`、`java.net.StandardSocketOptions`**；**JEP 444: Virtual Threads**（含 pinning 的讨论）；**JEP 380: Unix-Domain Socket Channels**。
* **Nasdaq TotalView-ITCH 5.0 规范与 MoldUDP64 规范**；**CME Group MDP 3.0 公开文档**：真实交易所的组播行情协议（序号、缺口检测、快照回补、A/B 线）。
* **DPDK 官方文档（dpdk.org）**；**Jens Axboe, "Efficient IO with io_uring"（2019）**：内核旁路与减少系统调用的两条路线。
* **Budish, Cramton, Shim, "The High-Frequency Trading Arms Race", Quarterly Journal of Economics 2015**：为什么微秒、微波链路在交易里值钱（经济学视角，了解背景用）。

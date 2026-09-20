---
nodes: [problems.media.video-conferencing]
tags: [solution]
---
# 设计题解：视频会议（Video Conferencing，Zoom）

## 题目与范围

面试官通常这样开场："设计一个类似 Zoom 的视频会议系统：多个用户加入同一个会议，
互相看到彼此的视频、听到彼此的声音，延迟要低到感觉像是面对面交流。" 这句话背后
真正的难点不是"传视频"，而是**媒体数据的路径必须绕开传统请求-响应式后端的思维**——
每个参会者既是发送方又是接收方，网络质量在通话过程中实时波动，而系统必须在毫秒
级做出"该丢什么、该降什么质量"的决策，这些决策一旦做晚了，用户体验就已经卡顿了，
没有"重试"这个选项。

值得当场问清楚的澄清问题，以及它们各自改变的设计决策：

- **典型会议规模是多少？1 对 1、小组会议，还是上千人的大型网络研讨会
  （webinar）？** 决定媒体转发架构是网状（mesh）、单点混流（MCU）还是选择性转发
  （SFU），本题按主流产品的真实选择——SFU 为主线设计，并在「深入探讨」第 1 节给出
  三者的带宽/算力对比（见「深入探讨」第 1 节）。
- **要不要支持端到端加密（E2EE）？** 决定媒体加密是只做"逐跳"（hop-by-hop）还是
  要在 SFU 转发的前提下额外做一层端到端加密（见「深入探讨」第 6 节）。
- **要不要支持录制？** 决定录制组件放在哪一层、以及它和 E2EE 的冲突怎么解决（见
  「深入探讨」第 7 节）。
- **弱网环境下优先保住什么？** 决定拥塞控制的降级顺序（见「深入探讨」第 4 节）——
  这个顺序不是随意的，音频比视频更不能丢。
- **要不要支持会中文字聊天？** 不做——聊天消息的可靠有序投递属于
  [[solution-chat-messaging]] 已经解决的问题，本题只在信令层预留一个数据通道
  引用，不重新设计。

**范围内**：信令面与媒体面的分离、NAT 穿透（STUN/TURN/ICE）、网状/MCU/SFU 的选择
与算力带宽对比、simulcast 与 SVC、拥塞控制与弱网降级、跨区域级联 SFU、录制、
端到端加密。**范围外**：会中文字聊天的可靠投递（见
[[solution-chat-messaging]]）、美颜/虚拟背景等客户端本地算法、日历集成与会议
调度、屏幕共享的编码细节（复用视频编码管线，不单独展开）。

## 需求

**功能需求（驱动设计的 3–5 条）**

1. 多个用户可以加入同一个会议，实时看到并听到彼此，音视频同步。
2. 网络条件变差时，系统自动降级（分辨率/帧率/关闭视频/纯音频），而不是让通话直接
   卡死或掉线。
3. 支持跨越不同网络环境（包括受限 NAT、企业防火墙）的用户互相建立媒体连接。
4. 会议可以被录制并保存供事后回看。
5. 会议规模可以从 1 对 1 扩展到数千人的网络研讨会，同一套核心架构承载两种场景。

**非功能需求（数字化）**

- **端到端媒体延迟**：交互式会议（非纯观看的网络研讨会）目标"口到耳"（mouth-to-
  ear）延迟 < 150ms——超过这个阈值，人类对话会出现明显的抢话/停顿，这是实时通信
  区别于其他题目最核心的一条硬指标，直接排除任何"先落盘再转发"式的架构。
- **建连成功率**：任意两个网络环境组合下，媒体路径建立成功率目标 > 99%（这是
  「深入探讨」第 2 节 TURN 中继必须作为兜底而不是可选项的原因——直连失败率不为
  零）。
- **可用性**：信令面（会议的创建/加入/离开控制）目标 99.95%；媒体面在单次通话
  内目标是"优雅降级而不是硬失败"——个别参会者的媒体连接中断不应该影响会议里其他
  人的通话。
- **一致性**：会议的参会者名单、静音状态等控制面状态要求强一致（所有人看到的
  "谁在麦"必须一致）；媒体流本身不追求任何一致性——丢包、乱序、跳变是实时媒体
  与生俱来的常态，由拥塞控制和编解码器自身处理，不是数据库层要解决的问题。

## 容量估算

**基础假设**（本设计的假设，不代表任何真实视频会议产品的数字）：日活参会人数
（DAU）3 亿；人均每天 1.2 次会议，平均会议时长 32 分钟，平均每场会议 4 名参会者。

```
会议开始次数/天 = 3×10^8 × 1.2 / 4 = 9.0×10^7
均值发起 QPS ≈ 9.0×10^7 / 86,400 ≈ 1,041.7

参会人次/天 = 3×10^8 × 1.2 = 3.6×10^8
参会人次到达速率 ≈ 3.6×10^8 / 86,400 ≈ 4,166.7 人次/秒
```

**并发参会人数用 Little's Law 算，而不是拍脑袋估**：一个人从加入到离开会议算作
一次"逗留"，逗留时长就是平均会议时长。

```
平均并发参会人数 = 到达速率 × 平均逗留时长 = 4,166.7 × (32×60) ≈ 8.0×10^6

这个 8×10^6 是全天 24 小时均匀分布下的平均值。会议使用高度集中在工作时段
（几个主要时区的上午 9 点到下午 6 点互相重叠的窗口），采用 ×4 的峰值系数（与
「通知系统」一题对突发聚集流量的处理同一量级）：

峰值并发参会人数 ≈ 8.0×10^6 × 4 = 3.2×10^7
```

**这是第一个决定架构的数字**：3200 万峰值并发参会人数，每个人都同时是媒体的发送方
和接收方，这个规模排除了任何依赖单一集中式服务器处理全部媒体转发的设计，必须水平
扩展到大量地理分布的媒体节点。

**媒体面的带宽/算力预算**（承接「深入探讨」第 1 节的每参会者带宽模型：上行
1.54Mbps，下行在"可见画面数上限"约束下约 5.1Mbps，合计约 6.64Mbps/人）：

```
单台媒体服务器按 10Gbps 网卡、6.64Mbps/人计算，可承载约 1,506 名并发参会者
峰值所需媒体服务器数 ≈ 3.2×10^7 / 1,506 ≈ 21,248 台
```

**交叉验证**：Discord 官方工程博客披露的真实数字是 260 万并发语音用户由 850+ 台
语音服务器承载（约 3,059 用户/服务器，见「来源与延伸」）。本设计算出的 1,506
人/服务器是纯语音的约一半，方向上完全符合预期——视频比纯语音的带宽需求高出一个
数量级，服务器可承载的并发人数理应更低，两者不是同一产品也不是同一媒体类型，这里
只做数量级方向上的合理性检验，不是精确对照。

**信令面**：信令是控制平面（加入/离开/静音状态/ICE candidate 交换），复用
「聊天与消息」一题里"单机可稳定维持约 10 万条长连接"的同一容量假设（同样是常规
商用长连接网关，没有理由假设这里单机连接容量数量级不同）：

```
峰值信令长连接数 ≈ 3.2×10^7（等同峰值并发参会人数，一人一条信令连接）
所需信令网关机器数 ≈ 3.2×10^7 / 100,000 = 320 台
```

信令面机器数（320 台）比媒体面（21,248 台）小接近两个数量级——这个对比本身就是
「高层设计」要把信令面和媒体面拆成两套独立可扩展系统的数字依据：控制逻辑轻量，
媒体转发才是真正吃资源的部分。

## 核心实体与 API

**实体**

- **Meeting**：`id, hostId, createdAt, status(active/ended), region, e2eeEnabled`——
  会议的控制面根实体。
- **Participant**：`id, meetingId, userId, joinedAt, mediaState{videoOn, audioOn,
  screenShareOn}， signallingConnId`——每个参会者在这场会议里的状态，和「聊天与
  消息」一题的会话目录（session directory）是同一类"谁在哪"的轻量记录。
- **MediaSession**：`participantId, sfuNodeId, iceState, activeLayers[]`——一个
  参会者与其所在 SFU 节点之间的媒体连接状态，`activeLayers` 记录当前正在收发的
  simulcast/SVC 层（见「深入探讨」第 3 节）。
- **RecordingJob**：`meetingId, status, storageRef, startedAt, stoppedAt`——录制
  任务，见「深入探讨」第 7 节。

**API**（信令走持久连接为主，REST 为辅）

```
POST   /meetings                        → {meetingId}
POST   /meetings/{id}/join               → {signallingWsUrl, iceServers[],
                                            sfuNodeAssignment}
WSS    /signal?meetingId=&participantId= 信令长连接：交换 SDP offer/answer、
                                          ICE candidate、静音/摄像头状态变更
POST   /meetings/{id}/leave              离开会议，释放 MediaSession
POST   /meetings/{id}/recording/start    启动 RecordingJob
POST   /meetings/{id}/recording/stop     停止并落盘
```

**故意不做的**：不在应用层 API 暴露媒体字节本身（媒体走独立的 UDP/SRTP 路径，
不经过这套 HTTP/WS API）；不支持客户端直接指定使用哪个 SFU 节点（由服务端按
地理位置和当前负载分配，见「深入探讨」第 5 节）；不做客户端本地录制的服务端管理
（本地录制是设备存储问题，不是这道题的服务端设计范围）。

## 高层设计

```mermaid
flowchart TB
    subgraph Signalling["信令面（Signalling Plane）"]
        ClientA["参会者 A"] -->|WSS| SigGW["信令网关"]
        ClientB["参会者 B"] -->|WSS| SigGW
        SigGW --> SessDir[("会话目录<br/>谁在哪个 SFU 节点")]
    end

    subgraph NAT["NAT 穿透"]
        ClientA -.->|STUN: 发现公网候选地址| STUN["STUN 服务器"]
        ClientB -.->|STUN| STUN
        ClientA -.->|ICE 直连失败时| TURN["TURN 中继<br/>(见深入探讨2)"]
        ClientB -.->|ICE 直连失败时| TURN
    end

    subgraph MediaRegion1["媒体面 · 区域 A"]
        ClientA -->|SRTP simulcast 多层| SFU1["SFU 节点<br/>(选择性转发，不解码)"]
        SFU1 --> ClientB
        SFU1 --> Recorder["录制 Bot<br/>(见深入探讨7)"]
    end

    subgraph MediaRegion2["媒体面 · 区域 B（大型会议级联）"]
        SFU1 -->|区域间只转发一份<br/>(见深入探讨5)| SFU2["级联 SFU 节点"]
        SFU2 --> ClientC["参会者 C (区域 B)"]
    end

    SigGW -.->|分配 SFU 节点, 触发 ICE 协商| SFU1
    Recorder --> ObjStore[("对象存储<br/>(录制文件)")]
```

**信令面**：加入会议时，客户端先通过 `POST /meetings/{id}/join` 拿到分配的 SFU
节点和 ICE 服务器列表，随后建立到信令网关的持久 WebSocket 连接，用于交换 SDP
（会话描述）和 ICE candidate——这一整套协商过程本身不传输媒体字节，只是"约定
怎么传"。信令网关是无状态的，真正的"谁在哪"记录在轻量的会话目录里，和「聊天与
消息」一题的会话目录是同一个模式。

**NAT 穿透**：每个客户端先向 STUN 服务器查询自己的公网可达地址（server-reflexive
候选），尝试和对端直连；如果双方 NAT 类型不兼容导致直连不可行（见「深入探讨」
第 2 节），才退化到通过 TURN 服务器中继媒体——这是 ICE（RFC 8445）定义的标准
候选收集与优选流程，直连优先、中继兜底。

**媒体面**：客户端把自己的音视频用 simulcast 编码成多个质量层，通过 SRTP 发送
给分配到的 SFU 节点；SFU **不解码媒体内容**，只根据每个接收端当前的网络状况和
渲染需求，为每个接收端选择并转发合适的层（见「深入探讨」第 3 节）——这正是 SFU
相对 MCU 最大的架构优势，也是它能达成前面算出的 21,248 台服务器（而不是数量级
更高）这一容量结论的原因。大型会议跨区域时，SFU 节点之间级联，媒体只在区域之间
传输一份，由目标区域的 SFU 再向本地参会者扇出（见「深入探讨」第 5 节）。

## 深入探讨

### 网状（mesh）、单点混流（MCU）与选择性转发（SFU）：为 N 个参会者算出的带宽与算力账

**问题**：多方通话有三种架构，选错一种在参会人数增长时会直接把带宽或服务器算力
需求推到不可行的量级。假设每路音视频流稳定占用 1.54Mbps（1.5Mbps 视频 + 40kbps
音频，本设计假设）。

**方案一：网状（mesh）**，每个客户端直接和其余 N-1 个参会者建立点对点连接，各自
把自己的编码流发给每一个对端：

```
N=6 时：每个参会者上行 = 下行 = (N-1)×1.54Mbps ≈ 7.70 Mbps（同时收发）
N=10 时：≈ 13.86 Mbps；N=25 时：≈ 36.96 Mbps
```

典型家庭宽带的上行带宽通常在 5–20Mbps 区间且往往低于下行——N=6 时 7.70Mbps 的
**上行**需求已经逼近很多消费级宽带的上限，这还只是单个参会者的账，mesh 的总网络
流量随 N² 增长，是三种方案里唯一"参会人数翻倍、带宽需求翻两番以上"的架构，只适合
2–3 人的通话。

**方案二：单点混流（MCU）**，服务器把收到的全部 N 路流完整解码、合成
（mix/composite）成一路画面（比如网格布局）加一路混合音频，再编码发给每个参会者：

```
每个参会者上行 = 下行 = 1.54Mbps（恒定，与 N 无关）——对参会者带宽最友好
```

代价转移到了服务器算力上。假设一个 CPU 核心能实时解码约 12 路 1080p 流、但只能
实时编码约 4 路（编码涉及运动估计和码率-失真优化，是解码的数倍开销，这是编解码器
的普遍结构性事实，不是某个具体产品的数字）：

```
N=25 人会议，单一共享合成画面：
所需核心 ≈ 25 路解码/12 + 1 路编码/4 = 2.08 + 0.25 ≈ 2.33 核/会议

若要求千人千面（每个参会者看到不同的高亮/布局，需要单独编码）：
所需核心 ≈ 25/12 + 25/4 ≈ 2.08 + 6.25 ≈ 8.33 核/会议
```

MCU 的算力成本随 N 增长（解码侧），个性化视图时编码侧成本还会再乘上 N——这是 MCU
在现代产品里退居为"遗留终端兼容网关"（比如接入传统会议室硬件或 PSTN 电话）而不是
默认架构的根本原因。

**方案三（本设计采用）：选择性转发（SFU）**，服务器只做转发决策，不解码、不重新
编码，把收到的每路流原样转发给需要它的接收端：

```
每个参会者上行 = 1.54Mbps（恒定，只发自己这一路）
每个参会者下行 = (N-1)×1.54Mbps（若不加约束，literal 转发全部其他人的流）
服务器算力 ≈ 纯网络 I/O 转发，不含解码/编码开销，同样规模下比 MCU 低一到两个数量级
```

SFU 把 MCU 的"服务器算力爆炸"问题换成了"接收端下行带宽随 N 增长"的问题——如果
真的对每个接收端转发全部 N-1 路完整分辨率的流，N=25 时下行需求高达 36.96Mbps，
对接收端消费级宽带同样不可行。解法不是回到 MCU，而是让 SFU 只转发**接收端当前
真正用得上的层**——见「深入探讨」第 3 节的 simulcast/SVC——这一步做完之后，SFU
才是三种方案里唯一能同时把参会者带宽和服务器算力都控制在可行范围内的架构，这也是
主流产品的真实选择。

### NAT 穿透：ICE、STUN、TURN，以及"中继"为什么必须是兜底而不是可选项

**问题**：绝大多数参会者都在某种 NAT（网络地址转换）后面，两个都在 NAT 后面的
客户端不能简单地互相知道对方的可达地址，更麻烦的是，某些 NAT 类型（对称型 NAT，
symmetric NAT）会让"打洞"（hole punching）类技术从根本上失效——不是概率低，是
协议层面必然失败。

**ICE（RFC 8445）定义的候选收集与优选流程**：每个客户端收集三类候选地址——
主机候选（本地网卡地址）、服务器反射候选（server-reflexive，通过 STUN 服务器
询问自己的 NAT 映射出的公网地址）、中继候选（relayed，向 TURN 服务器申请的一个
中转地址）。双方交换全部候选后，两两配对做连通性检查，按优先级（直连 > 服务器
反射 > 中继）选出真正能用的一对。

**为什么中继不能是"极端情况才需要"的可选组件**：RFC 8656 明确指出，当双方都在
"地址依赖"或"地址端口依赖"映射行为的 NAT 后面时，打洞技术必然失败，必须用 TURN
中继。这类 NAT 在企业防火墙和部分运营商级 NAT（CGNAT）后面相当常见。本设计假设
（未经来源验证，作为本设计的容量输入）约 15% 的参会连接无法建立直连或服务器反射
路径，必须回退到 TURN 中继：

```
峰值并发参会人数 3.2×10^7 × 15% = 4.8×10^6 人需要中继
中继服务器同时要接收和转发同一份媒体字节（进 + 出），以 NIC 吞吐量计算，
单台中继服务器有效承载能力仅为普通媒体转发节点的约一半：
≈ 3.2×10^7 × 15% / 753 ≈ 6,374 台中继服务器
```

RFC 8656 原文特别强调 TURN 中继"对服务提供方而言成本很高"，这个数字正是这句话
的具体量化——中继不是媒体路径的性能优化选项，是必须为"直连失败"这个不可避免的
子集单独预留、且单价更高的一层基础设施。

### Simulcast 与 SVC：让每个接收端只拿到它用得上的那一层

**问题**：「深入探讨」第 1 节已经指出，SFU 如果对每个接收端转发全部其他参会者的
完整分辨率流，下行带宽随 N 线性增长，N=25 时已经不可行。而且不同接收端的网络
质量和渲染需求天差地别——一个只在小方格里显示某人画面的接收端，不需要那个人的
720p 完整分辨率流。

**方案一：Simulcast**。发送端同时编码并上行多个独立的质量层（比如同时编两路
或三路：1080p、360p、180p，各自独立的比特流）。SFU 不需要转码，只需要根据每个
接收端的请求，从这几路里选一路转发给它——网络好、要放大看的接收端拿高层，网络差、
只需要缩略图的接收端拿低层。代价是发送端要同时编码多路（编码本身的 CPU 开销
是解码的数倍，发送端要多付出这部分算力和上行带宽，但只是几倍而不是随 N 增长）。

**方案二：SVC（可分层视频编码，Scalable Video Coding）**。发送端只编码**一路**
比特流，但内部按空间/时间维度分层（base layer + enhancement layers)，SFU 可以
直接丢弃高层的 NAL 单元来降级，不需要发送端准备多路独立编码。比 simulcast 更省
发送端带宽和 SFU 存储，但编解码器和网络中间设备的支持度不如 simulcast 成熟普及，
是更新但兼容性要求更高的方案。

**结论（本设计以 simulcast 为默认，把 SVC 作为可协商的编解码能力）**：结合
「深入探讨」第 1 节的"可见画面数上限"约束——一个典型的会议 UI 一次只完整渲染
少数几个参会者（比如当前发言人 + 几个缩略图)，SFU 只需要为这一小部分接收对象
转发中高层，其余参会者的音视频只需要极低码率的缩略图层甚至只转发音频：

```
下行带宽（tile 数上限模型）= 1 路发言人高层(1.5Mbps) + 24 路缩略图低层(各 0.15Mbps)
≈ 1.5 + 24×0.15 = 5.1 Mbps

而不是「深入探讨」第 1 节里 literal 转发全部 N-1 路的 36.96Mbps（N=25 时）
```

这正是「容量估算」一节里 6.64Mbps/人（1.54 上行 + 5.1 下行）这个数字的来源——
simulcast/SVC 不是锦上添花的优化，是让 SFU 架构在参会人数增长时保持可行的必要
机制。

### 拥塞控制与弱网降级：先丢什么、最后才丢什么

**问题**：网络状况在通话过程中持续波动，编码码率如果一直按最理想网络设置，一旦
带宽收窄就会导致排队延迟暴涨甚至丢包雪崩；但降级也不能是"一刀切掉视频"，要有
优先级。

**拥塞检测（本设计采用 Google Congestion Control 一类的方案，GCC）**：发送端
的码率决策来自两个独立估计器的较小值——基于丢包率的估计器，以及**基于延迟梯度
的估计器**：后者通过比较连续数据包组的实际到达间隔和发送间隔，在真正出现丢包
**之前**就能检测到网络排队正在累积（拥塞的早期信号），从而提前降码率，而不是等
丢包发生后才被动反应。检测到过载时，估计带宽按一个乘性因子（GCC 草案里典型值
约 0.85）快速下调；网络恢复时则缓慢爬升，这种"快降慢升"的不对称正是为了避免
振荡。

**降级顺序（本设计采用，与任务给定的优先级一致）**：分辨率/码率 → 帧率 → 关闭
视频 → 音频最后。理由是信息价值和带宽成本不对称——音频码率本身只有 24–40kbps
量级，即便网络降到几乎不能视频通话的程度，这点带宽通常仍然挤得出来，而语音是
"对话是否还能继续"的最后一道底线；视频先降分辨率（比如从 720p 降到 360p，编码器
按新的目标码率重新编码或 SFU 直接切到 simulcast 的低层)、再降帧率（比如从 30fps
降到 15fps，对人眼的观感损失小于分辨率骤降)、最后才整体关闭视频只保留音频——这个
顺序保证了"通话是否还能进行"这条最重要的体验曲线，退化得比画质曲线更慢。

### 跨区域级联 SFU：大型会议如何避免让骨干网带宽随观众数线性增长

**问题**：一场上千人参与、少数几位主讲人的网络研讨会（webinar），如果全部观众
不论所在地区都直接向同一个区域的 SFU 拉流，该区域的出口带宽会随全球观众总数线性
增长，而且跨大洲的观众要忍受长距离传输带来的延迟和抖动。

**方案（本设计采用）：区域级联**。主讲人的流只需要送到源区域的 SFU 一次；源区域
SFU 把这几路主讲人流，分别转发给其余每个区域各一份（不是每个观众各一份)，由每个
区域自己的 SFU 节点再向本区域内的观众做本地扇出。假设 1000 人会议、5 位主讲人、
观众均匀分布在 5 个区域（每区约 199 人)，对比两种方案：

```
不做级联（全部观众直连源区域 SFU）：
源区域出口带宽 = 995 × (5×1.5Mbps) = 995 × 7.5Mbps ≈ 7,462.5 Mbps ≈ 7.46 Gbps

区域级联：
跨区域骨干网流量 = 4 个远端区域 × 5 路主讲人流 × 1.5Mbps = 30 Mbps（与观众数无关！）
各区域本地扇出 = 199 × 7.5Mbps ≈ 1,492.5 Mbps/区域 × 5 区域 ≈ 7,462.5 Mbps（同前，
但发生在区域内部的本地网络，不占用昂贵的跨区域骨干链路）
```

关键的数字对比是**跨区域骨干网流量从"和观众总数成正比"变成"只和(主讲人数 × 区域
数)成正比"**——30Mbps 不随观众规模增长，这正是级联架构要解决的问题，而不是简单地
"多加几台服务器"。

### 端到端加密（E2EE）穿过一个必须转发的 SFU

**问题**：标准做法是 SRTP 做**逐跳**（hop-by-hop）加密——客户端到 SFU 一段密钥，
SFU 到另一端客户端再一段密钥，SFU 中间必然持有明文才能完成 simulcast 层选择
这类转发决策。这意味着运营 SFU 的一方原则上能看到媒体明文，不满足"只有参会双方
能解密"的端到端加密要求。

**方案一：不做端到端加密，只信任传输层加密（SRTP 逐跳）**。实现简单，SFU 可以
自由做转码和层选择，但服务提供方处于"能看到内容"的信任位置，不满足高敏感场景
（法律咨询、医疗、企业机密会议）的合规要求。

**方案二：SFU 转 MCU，在服务器侧解密做媒体处理**。彻底放弃端到端加密，不是
真正的解法。

**方案三（本设计采用）：SFrame（RFC 9605）式的双层加密**。在标准 SRTP 逐跳
加密之外，再加一层**只有参会双方才持有密钥**的端到端加密，加密单位是媒体帧
（frame）而不是和 RTP 传输细节纠缠在一起。关键是 SFrame 的帧头（Key ID、
Counter）**不加密**，加上 simulcast 的分层天然是"每一层各自一个独立的密文"，
SFU 因此仍然可以只凭这些不加密的元数据做转发决策——选哪个 simulcast 层给哪个
接收端、丢弃哪些帧——完全不需要解密媒体内容本身。SFU 因此保留了它作为转发决策者
的全部能力，同时对媒体明文彻底不可见。

### 录制：在不破坏加密模型的前提下，录制组件应该长在哪一层

**问题**：录制需要拿到完整的、可解码的媒体内容才能落盘，但如果启用了端到端加密
（见上一节)，SFU 本身看不到明文——录制组件如果挂在 SFU 侧，天然拿不到能直接
写成文件的内容。

**方案（本设计采用）：录制机器人（recording bot）以"参会者"身份加入会议**，
而不是作为 SFU 内部的旁路组件。它和其他参会者一样，通过标准的媒体协商拿到属于
自己这一路连接的解密密钥（在 E2EE 场景下，这意味着录制必须被显式地当作"多一个
参会方"纳入密钥分发，而不是悄悄挂在基础设施里旁路窃听)，解密收到的各路流，按
布局合成或分轨保存，再写入对象存储。这个设计选择的好处是：录制的信任边界和普通
参会者完全一致——它能看到的内容，和它作为一个"人"能看到的内容没有区别，不会在
E2EE 之外开一个后门；代价是录制机器人本身要消耗和一个真实参会者同等量级的媒体
带宽与解码算力，数量随并发录制会议数线性增长，是独立于普通媒体转发容量之外的一项
单独预算。

## 瓶颈、故障与演进

**热点与倾斜**：媒体面的负载不是均匀分布的——大型网络研讨会的少数几个热门会议
（比如公司全员大会）会让某个区域的媒体服务器和录制机器人瞬间承受远超平均值的
并发，这是"会议级"的热点，而不是「信息流」一题那种"单条内容级"的热点，分配策略
需要按会议预估规模提前分配足够的 SFU 容量，而不是等负载已经发生再水平扩展（媒体
连接一旦建立，把一个参会者从一台 SFU 迁移到另一台意味着 ICE 重启，会有几百毫秒
到数秒的可感知中断)。

**故障域**：

- **单个 SFU 节点崩溃**：该节点上的参会者需要 ICE 重启（重新做一次 NAT 穿透
  协商）并连接到新分配的 SFU 节点，体验上是几秒钟的画面/声音中断，但不影响其他
  SFU 节点上的参会者——这是把媒体面拆成多个独立 SFU 节点而不是一个巨型集中式
  转发器的直接收益。
- **信令网关不可用**：进行中的媒体流不受直接影响（信令面和媒体面架构上解耦，
  媒体走独立的 SRTP 路径)，但静音状态切换、新参会者加入这类控制操作会失败，直到
  信令面恢复或客户端重连到健康的信令网关。
- **TURN 中继不可用**：依赖中继才能连通的那部分参会者（估算约 15%）无法维持
  媒体连接，而不依赖中继、能直连或走服务器反射地址的参会者不受影响——这是「深入
  探讨」第 2 节里"中继是兜底路径"的另一面，兜底路径本身也需要独立的高可用设计
  （多个区域的 TURN 集群，不是单点）。
- **录制机器人崩溃**：会议本身不受影响（录制机器人只是又一个参会者)，但这段
  时间的录制内容丢失，需要告警并支持从崩溃点重新加入继续录制（明确接受这段
  空档，而不是让整个会议为了保证录制完整性而暂停)。

**10 倍演进**：峰值并发参会人数从 3200 万到 3.2 亿。媒体服务器数量线性增长到约
21 万台，这个规模下，区域级联（「深入探讨」第 5 节）不再是"大型会议"的专属优化，
必须成为所有会议的默认路径，因为任何一个区域单独承载的媒体转发总带宽本身也会
触达该区域网络基础设施的物理上限。

**100 倍演进**：峰值并发参会人数 32 亿（纯粹推演）。此时 TURN 中继集群本身的
规模（约 63.7 万台，按当前 15% 中继比例线性外推）已经大到需要重新审视"能不能
把中继比例本身降下来"，而不是只靠堆机器——比如通过更激进地在客户端侧检测 NAT
类型并优先尝试 IPv6（很多受限 NAT 问题是 IPv4 NAT 特有的，IPv6 端到端可达性
天然规避了大部分对称 NAT 场景)，从需求侧压低中继依赖比例，而不是无限扩容供给侧。

## 面试官会追问什么

**中级（mid）**

- "为什么 1 对 1 通话可以用最简单的 P2P，但 3 人以上就不行了？" 期待候选人说出
  mesh 的带宽随 N-1 线性增长、且是同时上下行，N=6 时已经逼近典型家庭宽带上行
  上限（见「深入探讨」第 1 节），而不是含糊地说"人多了就复杂"。
- "客户端怎么知道自己的公网 IP？" 期待"通过 STUN 服务器查询 NAT 映射后的
  server-reflexive 地址"，而不是"客户端自己知道"这种误解。

**高级（senior）**

- "什么情况下会触发从视频降级到纯音频？" 期待候选人讲出拥塞控制检测到的可用
  带宽已经低于"哪怕最低码率视频"的下限，而不是"网络不好就关视频"这种没有阈值
  概念的回答；还应该提到这是「深入探讨」第 4 节降级顺序里的倒数第二步，音频
  才是最后底线。
- "Simulcast 和 SVC 有什么本质区别？" 期待候选人讲清楚 simulcast 是发送端编码
  多路独立比特流、SVC 是单路分层比特流，而不是把两者当作同义词。

**参谋级（staff）**

- "如果要支持一万人的网络研讨会，架构上需要改什么？" 期待候选人主动提出"可见
  画面数上限"这个思路本身已经让下行带宽与参会人数解耦（见「深入探讨」第 3 节），
  真正需要重新设计的是区域级联的扇出树形结构（见「深入探讨」第 5 节）要能支撑
  更深的级联层级，而不是简单说"加更多 SFU"。
- "启用端到端加密之后，录制怎么做？不会变成加密的后门吗？" 期待候选人讲出录制
  机器人必须以"参会者"身份显式参与密钥协商（见「深入探讨」第 7 节），而不是
  在基础设施层面悄悄拿到解密权——这是这道题里加密设计和产品功能设计直接冲突、
  需要显式取舍的地方。

## 常见错误

- 认为"视频会议就是很多个 WebSocket 连接"，完全没有区分信令面（控制)和媒体面
  （音视频字节本身走 UDP/SRTP，不是 WebSocket)。
- 把 MCU 和 SFU 混为一谈，说不清楚"服务器要不要解码"这个根本区别，也算不出两者
  算力/带宽账的具体数量级差异。
- 假设直连（P2P 或到 SFU 的直连）总是能成功，没有意识到 TURN 中继是协议层面
  某些 NAT 组合下必然需要的兜底路径，不是极端情况的可选优化。
- 弱网降级不分优先级，笼统地说"降低质量"，答不出"先降分辨率还是先关视频"这类
  追问，也说不出为什么音频要放在最后。
- 认为端到端加密和 SFU 转发天然矛盾，不知道 SFrame 这类帧级加密方案能让 SFU
  只凭不加密的元数据做转发决策而不需要看到媒体明文。

## 五分钟讲法

I'd frame Zoom-class video conferencing around one core tension: every participant is
simultaneously a sender and a receiver of real-time media, and there's no such thing as
retrying a late video frame. That immediately splits the design into a lightweight
signalling plane over WebSocket for call setup and a completely separate media plane
over UDP/SRTP for the actual audio and video, because the control logic and the media
forwarding have wildly different scaling properties — in my estimate, roughly two orders
of magnitude fewer machines for signalling than for media at the same concurrency. For
media forwarding itself, I'd rule out a full mesh past about five or six participants
since its bandwidth grows with the square of participant count and each person's uplink
alone exceeds typical home broadband; I'd also rule out a server that fully decodes and
re-mixes everyone's video, since that shifts an unbounded cost onto server CPU instead.
A selective forwarding unit that relays encoded packets without ever decoding them is
the right default, but forwarding every participant's full-resolution stream to every
receiver still doesn't scale, so senders encode simulcast layers and the SFU forwards
only the layer each receiver can actually use — full resolution for whoever's on screen,
a thin layer for the rest. Getting media between two peers at all requires NAT traversal
through ICE, preferring a direct or server-reflexive path via STUN and falling back to a
TURN relay only when the NAT types involved make direct connectivity structurally
impossible — and that fallback isn't rare enough to treat as an edge case, so relay
capacity has to be planned as its own, more expensive tier. Congestion control watches
for queueing delay building up before packet loss even happens, and degrades in a fixed
order that reflects how cheap audio is relative to video: resolution first, then frame
rate, then video off entirely, with audio protected until the very end since a few tens
of kilobits per second almost always survives even a bad connection. For a webinar-scale
meeting, presenter streams get sent once per region and fanned out locally by a cascaded
SFU rather than crossing expensive backbone links once per remote viewer, which decouples
inter-region bandwidth from audience size entirely. And end-to-end encryption doesn't
actually conflict with having an SFU in the middle — a frame-level encryption layer on
top of standard hop-by-hop SRTP leaves just enough metadata unencrypted for the SFU to
keep making forwarding decisions without ever seeing plaintext media, which also means a
recording bot has to join as a real participant under that same encryption, not sit
quietly inside the infrastructure with a decryption backdoor.

## 来源与延伸

- [RFC 8445 — Interactive Connectivity Establishment (ICE)](https://www.rfc-editor.org/rfc/rfc8445)、
  [RFC 8656 — TURN](https://www.rfc-editor.org/rfc/rfc8656)：定义了候选收集、
  连通性检查、直连优先/中继兜底的标准流程，以及中继对服务提供方而言成本高昂这一
  结构性事实。本题解「深入探讨」第 2 节的中继服务器容量估算直接建立在这一点上；
  15% 的中继比例是本题解自己的假设，RFC 本身不给出这类比例数字。
- [RFC 9605 — SFrame](https://www.rfc-editor.org/rfc/rfc9605)：定义了帧级端到端
  加密如何在 SFU 转发的前提下工作——帧头元数据不加密，使 SFU 能继续做层选择等
  转发决策而不需要解密媒体内容。本题解「深入探讨」第 6 节的 E2EE 方案直接采用
  这份规范描述的双层加密结构，并补充了"录制机器人必须以参会者身份参与密钥协商"
  这一节 RFC 本身没有展开的产品设计推论。
- [Google Congestion Control (draft-ietf-rmcat-gcc)](https://datatracker.ietf.org/doc/html/draft-ietf-rmcat-gcc-02)：
  定义了基于丢包和基于延迟梯度的双估计器拥塞控制算法，本题解「深入探讨」第 4
  节的"先于丢包检测到拥塞、快降慢升"直接来自这份草案描述的机制；本题解与它的
  差异在于：草案本身只定义带宽估计算法，没有规定"该先降分辨率还是先关视频"这类
  产品层面的降级优先级，这一顺序是本题解自己给出的论证。
- [Discord — How Discord Handles Two and a Half Million Concurrent Voice Users using WebRTC](https://discord.com/blog/how-discord-handles-two-and-half-million-concurrent-voice-users-using-webrtc)：
  披露了真实的语音服务规模数字（260 万并发用户、850+ 台语音服务器、13 个区域），
  以及他们为了简化架构选择完全不做 ICE、所有媒体强制经过自己的中继服务器这一
  和标准 WebRTC 不同的取舍。本题解「容量估算」一节用这篇文章披露的"用户数/
  服务器"比例，对自己算出的媒体服务器容量做了同一数量级的方向性交叉验证；本题解
  与它的分歧在于：本题解按标准 ICE 流程（直连优先、中继兜底）设计，而不是像
  Discord 那样为了简化直接放弃 ICE、让全部媒体都走中继。

---
nodes: [java-at-hft.where-java, java-at-hft.why-java, java-at-hft.java-vs-cpp, java-at-hft.how-fast, java-at-hft.talking-points, java-at-hft.career-ai]
tags: [drill]
---
# 练习：向面试官讲清「为什么在高频交易公司做 Java」

你在面试一家自营交易公司（proprietary trading firm，只用自己的钱交易）的 Java 软件工程师岗。面试官是 C++ 热路径团队的工程师，开口就问：「我们的交易引擎是 C++，你为什么觉得 Java 在这里有价值？Java 够快吗？你怎么证明自己写的 Java 尾延迟稳？」最后他还会让你提问。

**要你给出的**
- 一段 2 分钟的口头回答：一个观点、两条论据（各带数字）、一个你主动承认的代价。
- 三个追问各给 30 秒的答案。(1) Java 和 C++ 的边界在哪，数据怎么过边界；(2) 你报出的一个延迟数字，要说清哪五件事才可信；(3) AI 写代码越来越强，你的价值在哪。
- 从中选 3 个反问，每个写一句为什么问、好答案和坏答案各透露什么。

**评分要点**
- 先划清 Java 的位置：研究平台、分布式存储、计算集群、监控与内部工具、风控聚合与订单管理，这些系统重吞吐、业务复杂、需求变得快，延迟预算以毫秒甚至更宽计；纳秒到个位数微秒的交易引擎通常是 C++ 岗 ([[hft-java-at-hft-where-java-where]], [[hft-java-at-hft-java-vs-cpp-split]])
- 论据一，吞吐与迭代速度：试 1000 组参数、每组回测 1 小时，串行 1000 小时（约 42 天），100 台并行约 10 小时；能把回测快 2 倍、让集群利用率更高的工程师，直接让研究员一年验证更多想法。能 1 天回测完的公司一年约 250 轮，3 天的只有约 83 轮 ([[hft-java-at-hft-talking-points-throughput-latency]], [[hft-java-at-hft-talking-points-infra-edge]])
- 论据二，Java 的好处与坦诚的代价并说：内存安全（越界当场抛异常而不是悄悄改坏持仓）、开发速度、并发与可观测工具成熟、人才池大；代价是 GC、JIT、safepoint 带来的尾延迟，以及热路径要写得"像 C"。能说出边界在哪，比说"Java 什么都行"可信 ([[hft-java-at-hft-why-java-benefits]], [[hft-java-at-hft-why-java-costs]])
- 「Java 够快吗」按延迟预算回答：毫秒级普通 Java 加 G1；几十到几百微秒要调优（ZGC、零垃圾、绑核）；个位数微秒很难；纳秒到亚微秒用 C++ 或 FPGA。要在自己的负载上用 p99、p99.9 测，不用平均值 ([[hft-java-at-hft-why-java-fast-enough]], [[hft-java-at-hft-how-fast-vs-cpp-fpga]])
- 做到微秒级要四个前提：零垃圾、预热、绑核加核隔离、堆外内存与紧凑布局；缺一项都会在最关键的时刻慢一下 ([[hft-java-at-hft-how-fast-prerequisites]])
- 报延迟数字要说清五件事：测哪一段、哪个分位数、什么负载、多长的窗口（含不含 GC、预热、开盘高峰）、怎么测的（是否避开协同遗漏）；线程间传递一个事件 p50 约 100 ns，p99.99 可能是几十微秒到毫秒，只报 p50 会严重夸大 ([[hft-java-at-hft-how-fast-honest-numbers]], [[hft-java-at-hft-talking-points-measure-first]])
- 边界：用三个问题判断（10 微秒以内且尾部要稳 → C++；逻辑复杂变化快 → Java；深度依赖内核旁路或 FPGA 厂商接口 → C++）；跨语言边界要粗、只传扁平字节，一批消息放在同一块堆外内存里传地址和长度，用共享 schema 生成两边的编解码 ([[hft-java-at-hft-java-vs-cpp-decision]], [[hft-java-at-hft-interop-boundary]], [[hft-java-at-hft-interop-schema]])
- AI 的问题用三句话：承认它能写样板和第一版，区分它不知道你的机器和负载、错误只在尾部显现，举一个你亲手用测量发现问题的真实例子（例如 `getThreadAllocatedBytes` 发现某写法每次调用分配 32 字节）；AI 生成的 Stream、`Optional`、`HashMap<Long, ...>` 每秒 100 万次、每次 400 字节就是 400 MB/s 垃圾；反问要具体，别一上来问薪资 ([[hft-java-at-hft-career-ai-interview]], [[hft-java-at-hft-career-ai-hot-path-review]], [[hft-java-at-hft-talking-points-questions]])

**相关练习**：[[headlands/fit]]（简历逐条对职位描述）、[[headlands/01-company-brief]]（公司与岗位）、[[headlands/06-questions-to-ask]]（反问清单）、[[headlands/loop/LOOP_GUIDE]]（整场怎么走）、[[hc13_fixed_memory_pool]]（Java 里手管内存）、[[ld01_spsc_channel]]（共享内存单生产者单消费者通道）。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：

---
nodes: [orderbook.price-levels, orderbook.order-index, orderbook.memory-layout, orderbook.requirements, orderbook.testing]
tags: [drill]
---
# 练习：订单簿用了 std::map，p99 会从哪里来

一个团队这样写订单簿：价位放进 `std::map<Price, std::list<Order>>`（红黑树），订单索引用 `std::unordered_map<OrderId, Order*>`，每笔订单 `new` 一个节点，哈希表启动时没有预留容量。一只活跃股票有 1000 个价位、10 万笔在簿订单，开盘峰值每秒 100 万条消息，平均每条只有约 1 µs 的预算。

**要你给出的**
- 在看到任何测量之前先预测：p50、p99、p99.9 各自由什么造成，写成"原因 → 量级"。
- 重新设计三处：价位容器、订单索引、内存来源。每处写出你的选择、代价和它在什么情况下失效。
- 写出 4 条每处理完一条消息后都应该成立的不变量，用来检验重写后的簿。
- 回答：只有 20 个活跃价位时，为什么排序数组常比红黑树快；活跃价位到几千个时结论怎么变。

**评分要点**
- 消息分布决定设计：新增和撤单占绝大多数，成交很少，更新集中在买一卖一附近，所以撤单必须最快、取最优价的队首必须极快、热数据要紧凑 ([[hft-requirements-cancel-dominates]])
- 如果撤单要扫描：10 万笔订单平均扫 5 万笔，每笔 1 ns 也要 50 µs，是 1 µs 预算的 50 倍，队列就堆积，簿变成几毫秒前的状态 ([[hft-requirements-budget]])
- 红黑树：1000 个价位约 10 步，每步一次指针追逐，一次缓存未命中约 100 ns；100 万个键时 `TreeMap.get` 约 200 多纳秒，`HashMap.get` 约 10 纳秒。节点分散，还要旋转和分配 ([[hft-price-levels-tree]], [[hft-price-levels-choice]])
- 价格按 tick 换算成数组下标，查找、新增、删除都是 O(1)，没有比较和指针追逐；代价是价格范围要有界，范围太宽或精度太细（10^-8）会浪费内存，要维护最优价附近的窗口 ([[hft-price-levels-array]])
- 排序数组：最优价放末尾，20 个价位 8 字节共 160 字节约 3 条缓存行，中间插入用 `memmove` 只要几十纳秒；价位增到几百几千后挪动变贵，树或下标法更合适，结论要用真实行情回放验证 ([[hft-price-levels-sorted-vector]], [[hft-cpp-containers-sorted-vector-levels]])
- 订单索引：哈希表按订单编号找到订单，订单自己带前后指针（侵入式双向链表）在价位队列里 O(1) 摘除，撤单只要几十纳秒；开放寻址的扁平哈希表只触及 1 到 2 条缓存行、无分配 ([[hft-order-index-cancel-path]], [[hft-order-index-intrusive-list]], [[hft-cpp-containers-open-addressing]])
- 扩容和 rehash 是一次性的大操作：100 万个元素、每个 16 字节，搬一次约 16 MB、可到毫秒，旧指针全部失效；做法是启动时按峰值预留、负载保持在 50% 以下、运行中永不扩容 ([[hft-cpp-containers-rehash-spike]])
- 对象池加预触碰消除分配的不确定性；池会耗尽，要事先定好策略（拒绝、标记不可用或重启），并监控使用率 ([[hft-memory-layout-pool]], [[hft-memory-layout-exhaustion]])；不变量至少含：无负数量、价位总量等于订单之和、没有空价位、索引与簿一致 ([[hft-testing-invariants]])

**相关练习**：[[hc05_market_order_book]]（写订单簿与批量撮合）、[[hc13_fixed_memory_pool]]（定长内存池）。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：

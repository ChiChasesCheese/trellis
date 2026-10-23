---
nodes: [research-infra.research-to-prod, research-infra.compute-farm, research-infra.tick-capture, research-infra.time-series-db]
tags: [drill]
---
# 练习：回测很漂亮，实盘第一周就差了

研究员用 Python 回测一个做市策略，夏普比率（Sharpe ratio）很高；工程师用 C++ 重写后上线，第一周的盈亏明显差于回测。研究员接下来要对 5 个参数各取 10 个值做扫描，每次回测 10 分钟，每次回测要读一天约 1 TB 的行情。

**要你给出的**
- 列出"回测好、实盘差"的至少 5 类原因，每类写一个验证办法；说明怎样让两边用同一份代码，做不到时怎么办。
- 算：参数扫描的总计算量，单核要多少天，1000 个核要多久；一天 1 TB 的数据通过 10 Gb/s 网络（约 1.25 GB/s）搬一次要多久，由此说明为什么要让计算去找数据。
- 设计任务切分：某台机器挂掉，只重跑那一小块，结果还和原来一致，需要固定哪些输入。
- 说明行情为什么要录原始网络包并带硬件时间戳，一条 1 Gb/s 的线路一天大约多少数据，微突发为什么会丢包。

**评分要点**
- 常见原因：排队位置估得太乐观、延迟模型偏低、市场冲击、成本漏算、历史数据有缺口或时间戳不准、研究代码与生产代码不是同一份；排查是把实盘当天的输入灌进模拟器，对比"应得成交"与"实际成交" ([[hft-architecture-simulation-backtest-live-gap]], [[hft-architecture-simulation-queue-position]])
- 两份实现的差异很小但会叠加：例如 pandas 的 `rolling(20).mean()` 前 19 个点是 NaN 不产生信号，C++ 从第 1 个点就用已有数据算均值，开盘第一分钟信号就不同；缺失数据、浮点求和顺序、时间对齐也一样 ([[hft-research-infra-research-to-prod-gap]])
- 回测与实盘跑同一份策略代码，只替换事件来源和下单出口；必须有两份实现时用差分测试，同一天的数据喂给两边逐笔比较订单 ([[hft-research-infra-research-to-prod-shared-code]], [[hft-architecture-simulation-same-code-vs-two-codebases]])
- 回测的天花板：排队位置（前面 5000 股排完才轮到你）、市场冲击、延迟都无法精确复现；用影子模式让新策略吃实盘行情但不发单，与回测重放逐条对比。向量化回测容易有前视偏差，事件驱动在结构上排除它 ([[hft-research-infra-research-to-prod-backtest-ceiling]], [[hft-research-infra-research-to-prod-lookahead]])
- 扫描：10^5 = 100000 次回测 × 10 分钟 = 100 万分钟 ≈ 16667 小时 ≈ 694 天（单核）；1000 核约 16.7 小时；任务彼此几乎无依赖，天然适合并行 ([[hft-research-infra-compute-farm-why-cluster]])
- 数据本地性：1 TB ÷ 1.25 GB/s = 800 秒 ≈ 13 分钟，仅仅搬数据；1000 个任务都从中央存储读，网络先成为瓶颈、CPU 空闲。按日期和品种分片，任务派到有数据的机器；固定数据版本、代码版本、随机种子才能保证重跑一致 ([[hft-research-infra-compute-farm-data-locality]], [[hft-research-infra-compute-farm-reproducible-tasks]])
- 录制：保存原始包才能修好解码器后重新解码、保留到达顺序与重复丢失、精确回放；硬件时间戳纳秒级且不受 CPU 繁忙影响，经交换机镜像口或分光器送到独立抓包机器，不抢交易服务器的资源 ([[hft-research-infra-tick-capture-raw-packets]], [[hft-research-infra-tick-capture-hw-timestamps]])
- 体量与丢包：1 Gb/s = 125 MB/s，× 23400 秒（6.5 小时）≈ 2.9 TB；10 Gb/s 线路 1 ms 内可涌入 1.25 MB，缓冲区小于它就溢出；漏一个包，之后的订单簿全建立在错误状态上，回测盈利被高估。列式存储只读用到的列，行情分析因此普遍使用 ([[hft-research-infra-tick-capture-volume]], [[hft-research-infra-tick-capture-gaps]], [[hft-research-infra-time-series-db-columnar]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：

# 01 · 公司简报（Headlands Technologies · Software Developer / Java）

> 读者设定：不懂交易，基础概念偏薄。所以先讲"这是什么行业"，再讲"这家公司"，最后讲"JD 里的词"。每个因果都写出来。
> **引用格式**：`〔O-B1〕` = [catalog/raw/official_and_process.md](catalog/raw/official_and_process.md) 的 §B1（后面跟行名）；`〔O-C2〕` = Java JD；`〔O-G〕` = 文化表；`〔O-E〕` = 薪资；`〔O-D1〕` = 官方流程陈述。括号里的 `S1…S26` 是该文件 §A 来源台账的编号。
> 标 **（通识）** 的是行业常识，不是 Headlands 的来源，我用来帮你理解，不能当"Headlands 官方说"。标 **（推断）** 的是由事实推出来的判断，原文没有。
> 本文件不含任何面试官或招聘人员的姓名与邮件内容。

---

## 0. 一页结论

| # | 结论 | 出处 |
|---|---|---|
| 1 | Headlands 是**自营量化交易公司**：只用自己的钱交易，没有客户，没有外部投资人。 | 〔O-B1 自我描述 / 资金 / 公司做什么〕 |
| 2 | 你申请的 Java 岗**不在交易热路径上**：做的是"研究平台 + 分布式存储 + 计算集群 + 监控 + 网络延迟"这类基础设施。毫秒以下的交易引擎是 C++ 岗。 | 〔O-C2〕〔O-C3〕 |
| 3 | 官方给的 Java Chicago 基础薪资 **$175k–$300k**（只是 base）。 | 〔O-E 官方 careers 页〕 |
| 4 | 官方反复强调的人：好奇、独立、低自我、不要"朝九晚五"、需要懂很多层（数学 / 统计 / CS / 交易系统）。金融知识反而要得很少。 | 〔O-G〕 |
| 5 | 官方未公布人数、营收、技术栈细节。第三方说约 150 人，**不可靠**。 | 〔O-B1 规模〕 |
| 6 | 官方流程只有一句：2–3 周；JD 明说工程师参与面试并写评价，所以你面对的是"将来的同事"，不是 HR。 | 〔O-D1〕〔O-C2 Day to Day〕 |

---

## 1. 先把三种机构分清（通识）

你不需要懂金融才能通过面试（〔O-G 工程师要多少金融知识〕：官方原话是"Very little"）。但分不清这三个词，你会听不懂面试官的玩笑，也看不懂 JD 为什么这么写。

| | 自营交易公司（proprietary trading firm，prop firm） | 对冲基金（hedge fund） | 投资银行 / 券商（bank） |
|---|---|---|---|
| **谁的钱** | 公司自己的钱 | **别人的钱**（养老金、捐赠基金、富人）托管给基金 | 客户的钱（存款、委托交易）+ 银行自有资本 |
| **怎么赚钱** | 交易本身的利润，扣掉成本，全归公司 | 对客户收**管理费（约资产的百分之几）+ 业绩提成（超额利润的一部分）** | 手续费、撮合客户买卖的差价、借贷利差、承销费 |
| **有没有客户** | 没有 | 有（出资人） | 有（很多） |
| **持仓时间** | 做市 / 高频：秒甚至毫秒级；也有更长的策略 | 从天到数年，策略各异 | 视业务而定 |
| **技术的角色** | 技术**就是**产品：谁的系统更快、更稳、研究更快，谁赚钱 | 技术支持策略与风控 | 技术支持业务线与合规 |
| **监管** | 比银行轻，但仍要遵守交易所与监管规则 | 对出资人有披露义务 | 最重（资本充足率、合规） |

**因果**：因为 prop firm 用自己的钱，所以（1）没有"客户汇报""向出资人解释亏损"这类外部成本；（2）亏了是自己的钱，所以风险控制和系统可靠性被当成生存问题；（3）收入和公司业绩直接挂钩，所以官方说"incentivized based on just our performance and the firm's performance"〔O-G 激励机制，视频 08〕。

Headlands 自己的说法：「We are a privately funded company and do not accept outside investors.」〔O-B1 资金，S1〕；视频里："we trade all of our own internal capital"〔O-B1 资金，S4 视频 01〕；"We have no clients"〔O-G 公司做什么，视频 11〕。

对比：你之前准备过的 Millennium 是**对冲基金**里的"多经理平台"，见 [../millennium/01-company-brief.md](../millennium/01-company-brief.md)。同样雇 Java 工程师，两家的"产品"完全不同：Millennium 的技术服务几百个交易团队；Headlands 的技术服务一套自己的交易与研究系统。

---

## 2. 做市（market making）与量化交易，从零讲

### 2.1 市场怎么运转（通识）

股票交易所维护一本**订单簿（order book）**：所有人挂的"我愿意以这个价买 / 卖多少股"。

```
卖单 (ask)   100.03  x 500
             100.02  x 300
             100.01  x 200      <- 最低卖价 = best ask
-------------------------------- 价差 (spread) = 100.01 - 99.99 = 0.02
买单 (bid)    99.99  x 400      <- 最高买价 = best bid
              99.98  x 600
              99.97  x 100
```

**做市商（market maker）**：同时在买一和卖一附近挂单。有人想马上卖，就买他的；有人想马上买，就卖给他。做市商赚的是**价差**，并因此给市场提供"随时能成交"的**流动性（liquidity）**。

数字例子：在 99.99 买入 1000 股，在 100.01 卖出 1000 股，赚 1000 × (100.01 − 99.99) = **$20**。一次只赚 $20，所以要做**海量次数**，因此必须全自动。

### 2.2 为什么做市有风险，以及为什么这个风险叫"延迟"

你在 99.99 买了 1000 股，结果市场马上跌到 99.90：你亏 1000 × 0.09 = **$90**，要用 4.5 笔成功的往返交易才能赚回来。更糟的情形叫**逆向选择（adverse selection）**：对手比你**更早**知道价格要跌，所以专门在你的报价还没来得及撤时来打你。

→ **你的报价"过期"得越快被打，就越亏；你撤单、改价越快，就越安全。** 这就是低延迟（low latency）的经济学来源：不是"为了炫技更快"，是"慢一点就被做对手的人吃掉"。

Headlands 的一位研究员在官方博客里把这件事建模成期权：把你的报价看成一个"卖出的短期期权"，延迟相当于期权的到期时间；Black-Scholes 下到期时间减半，期权价格降约 30%（文中算出 29%）〔O-B2 #1，S10〕。检查一下：期权价值大致与 √T 成正比，√0.5 ≈ 0.707，即降约 29%。——意思是延迟减半，被"选择"的代价降约三成。

### 2.3 量化（quantitative）是什么

"量化"= 用数学、统计和程序来**研究**和**执行**交易想法，不靠直觉盯盘。官方自我描述：「designing and implementing cutting-edge quantitative trading strategies in an array of financial products on venues across the globe」〔O-B1 自我描述，S1〕；官方 2017 年博客列出了三类：套利（arbitrage）、market taking（主动吃单）、market making〔O-B1 交易品种，S6〕。

一个量化策略的一生（**通识**，与 Headlands 内部流程是否一致官方没写）：
1. 研究员提出假设（例如"某指标升高后，价格在 5 秒内上涨的概率更高"）；
2. 用历史数据**回测（backtest）**：把历史行情重放，看如果当时按这个规则交易会怎样；
3. 通过了才上线，上线后监控、对账、再调参。

第 2 步要读海量历史数据并重复成千上万次——这就是 JD 里"research platform""distributed storage""distributed computing farm"存在的原因，见 §4。

---

## 3. 为什么延迟重要，量级感

### 3.1 单位

1 秒 = 1,000 毫秒（ms）；1 毫秒 = 1,000 微秒（µs）。人眨一次眼约 100 ms；一次从内存读数据约 100 ns；下面的数字全在 µs–ms。

### 3.2 官方博客给的量级〔O-B2 #5，S6，经摘要器〕

| 环节 | 量级 |
|---|---|
| 一套较慢的软件系统，从收到行情到发出订单 | 约 30 µs |
| 交易所行情包之间的间隔 | 约 10–1,000 µs |
| 交易所撮合响应 | 约 100 µs – 5 ms |
| 纽约到芝加哥：微波 vs 光纤 | 约 4 ms vs 约 7 ms |

最后一行可以自己验证（**推断**，通识物理）：纽约到芝加哥直线约 1,150 km。真空中光速约 300,000 km/s，1,150 / 300,000 ≈ 3.8 ms，与微波的 4 ms 吻合；光在光纤里慢约三分之一（约 200,000 km/s），再加上光纤线路不是直线，所以约 7 ms。**因果**：为了省 3 ms，有公司愿意专门建微波塔——说明"几毫秒"在这行是真金白银。

### 3.3 工程上用的手段

官方博客点名的基线：生产系统用 C++（"rather than Python, R, or Matlab"）、co-location（把服务器放进交易所的机房，缩短物理距离）、Linux 调优（processor affinity 绑核、NUMA）、时钟同步〔O-B2 #5〕。

另一篇博客讲怎样让热路径更快：把很少用到的"冷数据"从对象里挪走，让热数据挤进同一缓存行，基准里快约 11.8 倍（作者称是人为构造的基准）〔O-B2 #3，S8〕。这是 **CPU 缓存局部性**（cache locality），Java 里的对应是对象布局与堆外内存，见 [study/00-foundations/cpu_cache_locality.md](study/00-foundations/cpu_cache_locality.md)。

### 3.4 对你的 Java 岗意味着什么

JD 的 Java 部分**没有**"exchange connectivity""lock-free""profiling"这些热路径词；这些词出现在同期 C++ 岗〔O-C3〕。Java 岗的 Day-to-day 里只有一条与延迟直接有关：「Improve networking communication between different components of the system to achieve optimal latency and throughput」〔O-C2〕——是**系统内部组件之间**，不是对交易所。（**推断**：Java 岗更偏研究平台与基础设施，〔O-C3〕末尾也是这个推断。）

---

## 4. JD 里的词：research platform、distributed storage、computing farm

JD 原文只给了词，没给内部结构〔O-C2〕。下面是用 §2–3 的因果**推出来的合理图景**，面试时当作"我的理解，请你纠正"来说，不要说成"Headlands 就是这样"。

### 4.1 一笔交易背后的系统（官方博客 2017 的组件表）〔O-B2 #5〕

```
 【实盘链路：必须极快】
 交易所 ──▶ market data parser ──▶ strategy ──▶ order gateway ──▶ 交易所
                                  ▲ 
 【配套】monitoring GUI · drop copy(交易所回传的成交副本) · market data capture(行情落盘) · 启动脚本

 【离线：不极快，但极大】
 参数优化 · production reconciliation(对账：实盘 vs 模拟是否一致) · backtesting simulator(回测) · 画图
 其中 tick 数据"可达每天数百 GB"
```

Java 岗大概率在**下面的"离线 + 配套"那一半**（推断）。

### 4.2 Research platform（研究平台）

= 研究员用来**提假设 → 取数据 → 回测 → 看结果**的内部软件。JD 说它是"proprietary"（自研）并要你 "improve performance and support new exchanges, products and functionality"〔O-C2 Scope〕。

**为什么要自研**（推断）：回测要和实盘用同一套"行情怎么解析、订单怎么模拟"的逻辑，否则回测结果不可信；而每新增一个交易所、一种品种，数据格式和规则都不同，所以平台要持续"支持新交易所、新产品"。

### 4.3 Distributed storage（分布式存储）

**为什么需要**：tick 数据"每天数百 GB"〔O-B2 #5〕。按交易日 250 天粗算（假设每天 200 GB，**这是我取的示例值，不是官方数**）：250 × 200 GB = 50 TB / 年，历史越长越大。一块盘装不下，也读不快（单盘顺序读约几百 MB/s，要读 50 TB 需要几十小时，计算：50,000,000 MB ÷ 500 MB/s = 100,000 s ≈ 28 小时）。所以数据要**切开放在很多台机器上**，并行读——这就是分布式存储。JD 要求："with various performance and reliability requirements"〔O-C2〕：有的数据要快（最近的 tick），有的要稳（不能丢的审计数据）——快和稳的取舍不同，设计也不同。

### 4.4 Distributed computing farm（分布式计算集群 / "农场"）

**是什么**：几百到几千台机器，研究员提交"跑一个回测 / 一批参数"的作业，调度器把作业分到空闲机器。类似你熟悉的 Spark / Kubernetes job，但是自建的（推断）。

**为什么需要**：假设要试 1,000 组参数，每组回测 1 小时（示例值）。串行 = 1,000 小时 ≈ 42 天；100 台并行 ≈ 10 小时。研究员的迭代速度 = 公司研究产出的速度。

JD 对应：「Investigate new technologies to improve stability, scalability, and performance of a distributed computing farm」〔O-C2〕；「Perform basic data analysis to support decision making and better plan for future growth」= 看作业量、磁盘增长，决定什么时候加机器〔O-C2〕；「Develop and improve monitoring and proactive detection capabilities」= 机器、作业、数据质量出问题要**先于研究员**发现〔O-C2〕。

### 4.5 24 小时、全自动

官方视频 14：交易周从芝加哥时间周日 16:00 到周五下午；芝加哥 24 小时有人值守，阿姆斯特丹、新加坡做冗余；并用一个比喻："how comfortable would you be on a commercial airliner if it was on autopilot but there were no pilots in the cockpit"〔O-G 24 小时运营，S4 视频 14〕。JD 的「large scale 24-hour automated trading system and research framework」〔O-B1 技术自述，S3〕同源。**因果**：系统不眠 → 变更不能随便停机、监控必须自动、测试必须充分 → 这就是 JD 为什么强调 "fully automated … with extensive testing"。

---

## 5. 公司事实

| 项 | 内容 | 出处 | 可信度 |
|---|---|---|---|
| 自我描述 | "A quantitative trading firm at the forefront of finance & technology. Since 2010 …" | 〔O-B1 自我描述〕S1 | 高 |
| 办公室 | Chicago（110 North Wacker Drive）· New York（520 5th Avenue）· Amsterdam · London · Singapore；"trade 24/7 across diverse financial markets"。Java 岗开放地点：Amsterdam / Chicago / London / New York。 | 〔O-B1 办公室〕S1；〔O-C1〕S3 | 高 |
| 成立 | 官网"Since 2010"；Wikipedia"July 2009"；Levels.fyi"2009"。**冲突，口头说"around 2010"最稳。** | 〔O-B1 成立时间〕 | 官网高 / 其余中 |
| 起步 | 2009 年 7 月 10 名员工，股票 / 期权 / 期货，不管理外部资金 | 〔O-B1 起步〕S11 | 中 |
| 创始人 | 三位前 Citadel 高管（其中一位现任 CEO，曾任 Citadel Securities 联席 CEO）；官网 bio 页已 404，只有 Wikipedia | 〔O-B1 创始人〕S11 | 中 |
| 固收业务 | 2013 成立电子固收子公司，2021 年 TD 收购该部分；Headlands 继续做股票 / 期权 / 期货自营 | 〔O-B1 固收业务〕S11 | 中 |
| 规模 | **官方未公布**；第三方估约 150 人 / 51–200 人，无日期。不要在面试里报数字。 | 〔O-B1 规模〕S12 | 低 |
| 营收 | 官方无；Levels.fyi 估算 $10M–$50M，口径与日期不明，**不采信** | 〔O-A 来源台账 S12〕 | 低 |
| 交易品种 | 官方只说"an array of financial products"；Levels.fyi：exchange-traded products incl. equities | 〔O-B1 交易品种〕 | 中 |
| 近期事件 | 2025-01 美国检察官指控一名前交易员窃取商业机密（Wikipedia） | 〔O-B1 近期事件〕S11 | 中；**面试中不主动提** |
| 官方技术博客 | 共 5 篇（2017–2024），无 Java 相关；与工程相关的是 2017 的 Quantitative Trading Summary、2018 的 OutOfLine（C++ 缓存局部性）、2024 的延迟竞争观点文 | 〔O-B2〕 | 高（正文经摘要器） |

### 薪资（只用官方）

| 岗位 | 基础薪资（Chicago） | 出处 |
|---|---|---|
| **Java Developer** | **$175k – $300k** | 〔O-E 官方 careers 页〕S2 |
| C++ Developer / C++ New Grad / Quant Researcher | $200k – $300k | 同上 |
| FPGA Engineer | $225k – $300k | 同上 |

- 只写了 **base**，没说奖金、是否有股权（官方写"based on our performance"〔O-G 激励机制〕）。（**推断**：自营公司总包通常显著高于 base，但官方没有数字。）
- Java 岗页面没有 New York 的福利 / 薪资区块；Amsterdam / London 未列金额。
- 福利（Chicago / New York）：医疗 day 1、HSA 公司注资、401(k) match、免费餐、健身房、月度 tech stipend 等〔O-E 官方福利〕。
- 第三方（Levels.fyi、H-1B 申报、Blind）在 raw 里有，但**可信度低或口径是底薪申报**〔O-E〕，不在此引用，也不要拿去谈判。
- 本文件不建议你主动谈薪；若被问期望，用 Millennium 的同款话术：先聊岗位，数字等到那个阶段。

---

## 6. 文化：他们自己的话

> 出处全部是官网首页的员工视频（我用本地语音识别转写，可能有错字，取意可靠）或 JD 〔O-G〕。官网没有"价值观"栏目。

| 他们说 | 原话（节选） | 对你的含义 |
|---|---|---|
| 要什么人 | "You kind of need to be good at everything … math, statistics, computer science, trading systems … we try to hire people that are different"（视频 03） | 面试官可能会测你是否"在不熟的层面也愿意往下挖" |
| 金融知识 | "Very little … you'll pick it up on the job … It's really having the problem solving ability that's foundational"（视频 17） | 别装懂金融，展示解决问题的能力 |
| 不合适的人 | "If you want the kind of job where you … work nine to five and then don't think about work at all, it's probably not a good fit … After a few years here, you're generally expected to have independent ideas"（视频 07） | 要显示主动性与长期的好奇心 |
| 好奇 | "we like to find entrepreneurs that are ever curious" ；讲了从小自己搭游戏服务器、升级电脑"curious why it was slow"（视频 12） | JD 的 "Genuine interest in solving technical problems" 的人格化 |
| 迭代快 | "I can kind of see what its impact on production within weeks. Whereas previously in the Big Tech, the rollout cycle could be months or even years"（视频 16） | 你在 PayPal 的 deploy 流程可以对比着说 |
| 无政治 | "no political games"；"You can walk into anyone's office including … any of the partners"；"everyone's ideas are treated pretty equally"（视频 09、13） | 对应 JD 的 "Low ego" |
| 激励 | 其他交易公司激励常按团队；这里"based on just our performance and the firm's performance"（视频 08） | 同上，团队不内耗 |
| 上手慢 | "maybe like even a year or two to get somebody up to speed"（视频 10） | 他们接受你要学很久，但要证明学得快 |
| 为什么现在 | "dominant player in many of the markets … new asset classes, new geographies … infrastructure that can be horizontally scaled"（视频 02） | 你的工作 = "水平扩展的基础设施" |
| 工程师价值词（JD） | "Low ego"、"collaborative"、"fully automated, scalable, and maintainable solutions with extensive testing"、"Genuine interest" | 见 [fit.md](fit.md)、[stories.md](stories.md) |
| 博客价值观 | "Attention to detail, hard work, trading intuition, and strong programming skills"（2017） | 细节 |

流程：官方一句话："two to three weeks is probably a good timeframe … very small team … move people through the process very quickly"〔O-D1，视频 19〕。完整面试结构见 [loop/LOOP_GUIDE.md](loop/LOOP_GUIDE.md)。

---

## 7. 我们不知道的（别在面试里假装知道）

1. Headlands 有多少 Java 工程师、Java 岗在组织里属于哪个组；
2. 研究平台的存储 / 调度具体用的是自研还是开源（JD 的 "open-source libraries" 暗示两者都有）；
3. 官方是否有 "NDA / 10 天 HackerRank 链接" 的统一安排（只有你自己收到的通知）〔O-缺口 4〕；
4. 2026 年的人数与营收；
5. Java 岗的真实面试题（全网没找到 Java 面经）〔O-F 5〕。

## 8. 术语速查

| 词 | 一句话 |
|---|---|
| prop firm | 用自己的钱交易的公司，无客户 |
| market making | 双边挂单赚价差并提供流动性 |
| spread | 最低卖价与最高买价之差 |
| adverse selection | 对手比你更早知道价格，专挑你的旧报价成交 |
| latency / throughput | 一件事要多久 / 单位时间能做多少件，二者常此消彼长（批量提高吞吐但增加延迟） |
| tick data | 逐笔行情，每笔报价 / 成交都记录 |
| backtest | 用历史行情重放策略，估计它过去会赚多少 |
| co-location | 服务器放在交易所机房里 |
| drop copy | 交易所给你的成交副本，用来对账 |
| reconciliation | 对账：两个系统的同一批数据是否一致 |
| compute farm | 一大批机器 + 作业调度，并行跑大量独立作业 |
| NUMA / affinity | 多路 CPU 的内存分区 / 把线程绑在某个核上，减少抖动 |

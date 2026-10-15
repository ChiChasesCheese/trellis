# LLD / OOD 练习路线：Amazon 最爱的 OOD 题（按真实被报告次数排序）

> 依据：`../catalog/raw/forums.md` §4.4（LeetCode Discuss / Reddit / 1point3acres 转述，2025-01..2026-10，110 条结构化报告，其中 SDE I 63 条）。
> 关键事实（forums.md §1）：**SDE I 的 63 条里有 43 条含 LLD/OOD，纯 HLD 轮 0 条**；SDE II+ 两者都考，且常把 LLD 说成 HLD 或反过来（LC6891316、JC-amz882）。
> 所以即使本 kit 的 bar 是 senior（见 `../AGENT_RULES.md`），**LLD 是岗位上最确定会出现的一轮**——与 `../sd/` 同等重要，建议先把 §2 的前 5 道做熟。
> 官方描述（`../catalog/raw/official.md` §4.3，逐字）：这一轮考的是 "Logical and maintainable"——"organize your methods and classes to ensure a clear separation of concerns … name variables, methods, and classes so future developers with no knowledge of the code can understand … Your test names should describe business and technical requirements"。
> 候选人描述（forums.md §1）：LLD 轮 30–45 分钟，写类、接口、核心方法，被追加 **5–6 条可扩展需求**；LC8293563："almost every one needed just a single line of code change"（这就是评分标准）。

## 1. 一场 LLD 轮怎么跑（45 分钟）

官方三段式（official.md §4.2，逐字）："1. Uncover requirements and consider evolution of the situation. 2. Implement a first pass of the design and cover all requirements. 3. Enhance the solution. When you're satisfied you've met the original requirements, seek more requirements to show how your solution evolves when requirements change."

| 分钟 | 做什么 | 你要说出口的话 |
|---|---|---|
| 0–5 | 澄清需求：实体、核心操作、规模（单进程？并发？持久化？）、错误怎么表达 | "我先确认：谁是用户、核心操作 3–5 个、要不要线程安全、要不要持久化。" |
| 5–10 | 列实体与关系（类图草稿），挑出**会变的部分**（尺寸种类、折扣规则、过滤条件、费率） | "会变的部分我做成接口 / 策略；不会变的做成值对象。" |
| 10–30 | 写第一版：能跑通核心路径的类 + 关键方法（可运行的、语法正确的代码，不是伪代码） | 边写边说取舍；先简单后优化 |
| 30–40 | 面试官抛 5–6 条新需求：逐条说"改哪里"，**最好是加一个类 / 一行配置** | "这条需求我只需要新增一个 `XxxStrategy`，已有代码不动。" |
| 40–45 | 边界、测试、并发、复杂度；写 1–2 个测试用例的名字（测试名描述业务需求）| "我会写这几个测试：…" |

**评分要点**（official.md §4.3–4.4）：可读命名；类与方法职责单一；不写一个什么都干的大函数；没有伪代码；考虑边界/非法输入；能解释复杂度；测试名表达业务需求。

## 2. 题目排序（#refs 来自 forums.md §4.4；SDE I / SDE II+）

| 序 | 题 | SDE I / II+ refs | 本 kit / 题库里的位置 | 练习方式 |
|---|---|---|---|---|
| 1 | **File system / file search / filter API**（Unix `find`，"folder + filter → files"，AND/OR 组合，可扩展）| 8 / 6 | **本 kit 新写**：`file_search.md` + `code/file_search.py`；邻近：[lld:design-in-memory-file-system](../../../../domains/low-level-design/drills/problems/design-in-memory-file-system.md)（树本身）| 先自己做，再对照；重点练"加一种条件改几处" |
| 2 | **Amazon Locker** | 4 / 7 | 题库：[lld:design-amazon-locker](../../../../domains/low-level-design/drills/problems/design-amazon-locker.md)，解 [lld-solution:amazon-locker](../../../../domains/low-level-design/problems/amazon-locker/solution.py) | 题库自带 4 关 + pytest。Amazon 口味：JC-ibzau1 的追问 = "locations、S/M/L 格口、取件码带过期、release/return、并发、持久化表" |
| 3 | **Billing / pricing / fare / price-calculator**（AWS 账单、购物车折扣、披萨、地铁封顶、证券手续费）| 8 / 3 | **本 kit 新写**：`pricing_billing.md` + `code/pricing_billing.py`；邻近：[lld:design-online-shopping](../../../../domains/low-level-design/drills/problems/design-online-shopping.md) | 这是 SDE I 第二高频；5 个变体共用一个骨架 |
| 4 | **Rate limiter**（LLD 或分布式）| 3 / 7 | 题库：[lld:design-rate-limiter](../../../../domains/low-level-design/drills/problems/design-rate-limiter.md)，解 [lld-solution:rate-limiter](../../../../domains/low-level-design/problems/rate-limiter/solution.py) | 追问："固定窗口 / 滑动窗口 / 令牌桶；Redis；分布式一致性"（JC-amz882）；LC8535500 要求用 C++ 做 OOP |
| 5 | **Parking lot** | 5 / 2 | 题库：[lld:design-parking-lot](../../../../domains/low-level-design/drills/problems/design-parking-lot.md)，解 [lld-solution:parking-lot](../../../../domains/low-level-design/problems/parking-lot/solution.py) | 追问："多种车型、不同车位类别、5–6 条新需求"（LC8293563）；"按车型找最优车位"（LC8568929）；"停车票据/收据系统"（LC8525216）|
| 6 | **Logger / 日志框架** | 1 / 4 | 题库：[lld:design-logger](../../../../domains/low-level-design/drills/problems/design-logger.md)，解 [lld-solution:logger](../../../../domains/low-level-design/problems/logger/solution.py) | 追问："多种消息格式、字符串解析"（LC6397223） |
| 7 | **LRU / LFU cache** | 1 / 3 | 题库：[lld:design-lru-cache](../../../../domains/low-level-design/drills/problems/design-lru-cache.md)（含 LFU 讨论）、[lld:design-ttl-cache](../../../../domains/low-level-design/drills/problems/design-ttl-cache.md) | 经典；追问并发与淘汰策略可插拔 |
| 8 | **Recommendation / playlist / movie / Netflix 目录** | 1 / 3 | 题库：[lld:design-music-streaming](../../../../domains/low-level-design/drills/problems/design-music-streaming.md)、[lld:design-movie-booking](../../../../domains/low-level-design/drills/problems/design-movie-booking.md) | LC8468910：播放列表混音 DJ 服务 + 推荐服务，**纸上列 10 条需求**要写生产级类；RD1nfl6yl：Netflix 目录 + 暂停时记录"上次观看位置" |
| 9 | **Pub/Sub / 事件转发框架** | 1 / 3 | 题库：[lld:design-pub-sub](../../../../domains/low-level-design/drills/problems/design-pub-sub.md) | RD1qwi4zd："Subscribers and Actors：actors 发布事件，subscribers 接收"；LC6841317："event forwarding framework … batch, slow events, **failures must not block others**"（= 每个订阅者独立队列 + 失败隔离 + 重试/死信）|
| 10 | **Splitwise** | 0 / 3 | 题库：[lld:design-splitwise](../../../../domains/low-level-design/drills/problems/design-splitwise.md)（LC6891316 把它当 "Logical & Maintainable"）| 分摊零头用最大余数法（见 `pricing_billing.md` §2.2）|
| 11 | **Task / job scheduler** | 2 / 1 | 题库：[lld:design-task-scheduler](../../../../domains/low-level-design/drills/problems/design-task-scheduler.md) | RD1x1fmxc：白板上做，追问变需求"检查 OS 知识"（线程/阻塞）|
| 12 | **Bank / wallet / ATM** | 1 / 1 | 题库：[lld:design-bank-account](../../../../domains/low-level-design/drills/problems/design-bank-account.md)、[lld:design-atm](../../../../domains/low-level-design/drills/problems/design-atm.md) | LC8542502："deposit / credit / summary / tax，可扩展" |
| 13 | **Notification service / router** | HLD 与 LLD 混 | 题库：[lld:design-notification-service](../../../../domains/low-level-design/drills/problems/design-notification-service.md) | LC8315111：电商通知路由，考官期待 Strategy / Singleton / Factory |
| 14 | **Library management / Snake game / Stock broker / DNS 解析器（带健康检查、TTL、快速读）** | 各 1 | 题库：[lld:design-library](../../../../domains/low-level-design/drills/problems/design-library.md)、[lld:design-snake-and-ladder](../../../../domains/low-level-design/drills/problems/design-snake-and-ladder.md)、[lld:design-stock-brokerage](../../../../domains/low-level-design/drills/problems/design-stock-brokerage.md) | 长尾；做一遍即可。DNS 解析器（LC6841317）≈ TTL 缓存 + 健康检查：用 [lld:design-ttl-cache](../../../../domains/low-level-design/drills/problems/design-ttl-cache.md) 的思路 |
| 15 | **办公室人数追踪（presence tracker）** | 1 / 0（拿到 offer）| **本 kit 新写**：`occupancy_tracker.md` + `code/occupancy_tracker.py` | 小型数据模型 + 时间戳查询 + SQL |

**为什么这个顺序**：先做 #1–#3（本 kit 新写，且频次最高，题库没有），再回到题库做 #2、#4、#5（题库已有完整 4 关 + 测试），最后长尾。
建议总用时：新写的 3 道各 90 分钟（含重写一遍），题库的每道 60 分钟（只做第 1–3 关），长尾各 20 分钟看一遍题解。

## 3. 本 kit 新写三份的内容与运行

| 文件 | 解决的问题 | 运行 |
|---|---|---|
| `file_search.md` / `code/file_search.py` | 过滤器组合（Specification / Composite）、惰性遍历、符号链接环、剪枝、查询小语言 | `python3 -I code/file_search.py` → `OK file_search` |
| `pricing_billing.md` / `code/pricing_billing.py` | `Money` 值对象、规则引擎（策略 / 装饰器）、披萨 Builder、阶梯计价与免费额度、票价封顶、手续费 | `python3 -I code/pricing_billing.py` → `OK pricing_billing` |
| `occupancy_tracker.md` / `code/occupancy_tracker.py` | 事件溯源、前缀和 + 二分、可追加线段树、同一模型的 SQL 版 | `python3 -I code/occupancy_tracker.py` → `OK occupancy_tracker` |

题库的 pytest：在仓库根目录 `IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/<name> -q`（starter 是空壳，应该红；把你的实现填进去再跑；参考解用 `IMPL=solution`）。

## 4. 每道 LLD 题都要练的"扩展性演练"

面试官的 5–6 条新需求往往落在这几类里（来自 forums.md 的具体追问归纳，`推断` 为我的归纳）。每做完一道题，**不看代码**回答：

1. **加一种东西**（新尺寸 / 新过滤条件 / 新折扣 / 新车型）——应该是新增一个类或一行数据。
2. **改一条规则的顺序或优先级**——应该是改一个列表的顺序，而不是改算法。
3. **时间相关**（过期、封顶、有效期）——时间必须是注入的参数，代码里没有 `now()`。
4. **并发**——临界区覆盖哪几步？GIL 够不够？（题库的 Locker/Rate limiter 题解有现成讨论）
5. **持久化**——哪些是实体（要落库）、哪些是派生数据（可重建）？接口怎么不依赖具体存储？
6. **规模放大**——单进程 → 多进程 / 分布式：哪个对象变成服务？（可跳到 `../sd/` 的相应题）
7. **可观测 / 解释性**——这个结果为什么是这样？能打印一个 `explain()` 吗？（Customer Obsession）
8. **错误处理**——非法输入用什么异常类型表达？失败是否保持状态不变？

## 5. 和 SD 部分的对接
- LLD 题一旦被问到"并发 + 分布式"（JC-amz882 的 rate limiter、LC8457154 的"缓存文件内容、大文件担忧"滑入 HLD），就会转成系统设计：见 `../sd/route.md`。
- 官方 Senior SDE 低层设计视频（official.md §4.5）："detailed enough that if given to a team of junior engineers they could implement it correctly … be prepared to come up with class-level diagrams and if needed, code up the critical section … think what design patterns may be applicable … be vocal about trade-offs and assumptions"。

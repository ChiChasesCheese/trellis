# BUILD — low-level-design：2026-09 重构与题库

这份文件是这次重构的持久记录：调研了什么、骨架为什么长这样、为什么是这 45 道题、每一步做到哪、下一步做什么。
新会话从这里接手。方法见技能 `building-problem-banks`；所有数字由脚本算出，不是手数的。

## 1. 起点

重构前：英文域（`lang: en`），7 个分支、27 个叶子、125 张英中双语卡，**卡里的代码全是 Java**，中文是机翻质量；
经典面试题只作为 4 个 drill 存在，没有题库层。Anki 里 125 条笔记只有 10 条复习过，全在 `method` 分支——
重构时保住这 10 个卡片 id，其余放手重写。

## 2. 调研（2026-09-20，GitHub 优先）

- [[lld-survey-github]]：10 个仓库，逐个读了 LICENSE（6 个没有 LICENSE 文件；`abhaypaswan/lld-python` 是 MIT 且带 pytest；
  `system-design-primer` 的 OOD 部分是 CC BY，Python；`kumaransg/LLD`、`InterviewReady` 确认为纯 Java）
- [[lld-survey-prep-sites]]：Hello Interview LLD 指南与题解、Educative 与 DesignGurus 的两门 Grokking、AlgoMaster、Codemia、workat.tech、Refactoring.Guru；
  各课程的完整大纲抄录在案，是概念层骨架的依据
- [[lld-survey-companies-python]]：带公司标签的真题来源、分关递进的机考题型、Python 专属设计资料（python-patterns.guide、Fluent Python、cosmicpython、官方文档）

合计 **376 行题目、21 个来源、85 个去重后的题名**。本会话 WebSearch 配额在调研中途用尽，
之后只能直连已知 URL；CodeZym、GeeksforGeeks 等几个来源因此未能覆盖（原始文件的 Notes 里逐条记了试过的路径）。

### 概念层骨架（40 个叶子）

各家大纲的并集：作答方法、OOP 概念、类关系、UML、设计原则、设计模式（逐个）、并发、整洁代码与重构。对照旧骨架的改动：

- 新分支 **Python 对象模型与惯用法**（7 个叶子）：数据模型、dataclass 与 Enum、Protocol 与 ABC、一等函数、上下文管理器与迭代器、类型注解、模块与依赖方向。
  这是 Java 式答案与 Python 式答案的分叉点，旧骨架完全没有。
- **设计模式**从 3 个粗叶子拆出面试最常考的四个：策略、观察者、状态、命令；其余行为型模式合为一个叶子。每个模式都回答「Python 里还需要它吗」。
- 新叶子：白板上的 UML、asyncio 与协程；并发分支改为从 GIL 讲起。
- 仍成立的叶子保留原 id，卡片与复习记录不受影响。

### 题库入选线

**至少被 3 个独立来源当作一道题来教** → 43 道。另按判断补入 2 道并发题（线程池、有界阻塞队列）：调研到的题单多为 Java 课程的
「业务对象」目录，并发类题目被系统性低估，而 Hello Interview 用三章专讲并发题型。合计 **45 道**，分 6 个家族，
家族与叶子按来源数排序；来源数最高的 10 道标为 `core: true`。别名折叠规则在 `scripts/lld_problem_aliases.py`。

范围外：纯数据结构练习（哈希表、栈与队列实现）、专门领域（编译器、物理引擎、ECS）、其实是系统设计的题（视频会议、视频平台），共 8 个题名。
观察名单（1–2 个来源）：Payment method ranker（2）、Payment gateway（2）、Online judge（2）、Course registration（2）、Billing / discount engine（2）、Workout planner（1）、Voting system（1）、State machine / workflow engine（1）、Spreadsheet（1）、Service orchestrator（1）、Ride surge-pricing engine（1）、Resource management system（1）、Plugin system（1）、Pharmacy management system（1）、Permission and role system（1）、Object pool（1）、Middleware chain（1）、Learning management system（1）、Jigsaw puzzle（1）、IoT smart home system（1） 等 33 个。

## 3. 覆盖矩阵（按来源数排序）

| 来源数 | 其中带 Python 代码的免费来源 | 叶子 | 题目 | 核心 |
|---|---|---|---|---|
| 16 | 4 | `problems.machines.parking-lot` | 停车场（Parking Lot） | ✓ |
| 14 | 2 | `problems.machines.elevator` | 电梯系统（Elevator System） | ✓ |
| 13 | 1 | `problems.booking.movie-booking` | 电影订票（BookMyShow） | ✓ |
| 13 | 1 | `problems.marketplaces.splitwise` | 分账（Splitwise） | ✓ |
| 11 | 1 | `problems.games.chess` | 国际象棋（Chess） | ✓ |
| 11 | 0 | `problems.marketplaces.online-shopping` | 在线购物（Amazon） | ✓ |
| 11 | 0 | `problems.marketplaces.ride-sharing` | 网约车（Uber） | ✓ |
| 10 | 1 | `problems.machines.vending-machine` | 自动售货机（Vending Machine） | ✓ |
| 10 | 2 | `problems.components.lru-cache` | LRU / LFU 缓存 | ✓ |
| 9 | 0 | `problems.social.social-network` | 社交网络（Social Network） | ✓ |
| 8 | 1 | `problems.machines.atm` | ATM 取款机 |  |
| 8 | 2 | `problems.games.tic-tac-toe` | 井字棋（Tic-Tac-Toe） |  |
| 8 | 1 | `problems.games.snake-and-ladder` | 蛇梯棋（Snake and Ladder） |  |
| 8 | 0 | `problems.games.cricinfo` | 体育比分系统（Cricinfo） |  |
| 8 | 0 | `problems.marketplaces.stock-brokerage` | 股票交易系统（Stock Brokerage） |  |
| 8 | 1 | `problems.components.logger` | 日志框架（Logging Framework） |  |
| 8 | 2 | `problems.components.in-memory-file-system` | 内存文件系统（In-Memory File System） |  |
| 7 | 0 | `problems.booking.hotel-booking` | 酒店预订（Hotel Booking） |  |
| 7 | 0 | `problems.booking.car-rental` | 租车系统（Car Rental） |  |
| 7 | 0 | `problems.booking.library` | 图书馆管理（Library Management） |  |
| 7 | 0 | `problems.marketplaces.food-delivery` | 外卖配送（Food Delivery） |  |
| 7 | 1 | `problems.components.notification-service` | 通知服务（Notification Service） |  |
| 7 | 0 | `problems.components.pub-sub` | 发布订阅与事件总线（Pub-Sub） |  |
| 6 | 0 | `problems.booking.airline` | 航班管理（Airline Management） |  |
| 6 | 0 | `problems.booking.meeting-scheduler` | 会议室预订（Meeting Scheduler） |  |
| 6 | 0 | `problems.booking.restaurant` | 餐厅管理（Restaurant Management） |  |
| 6 | 1 | `problems.components.rate-limiter` | 限流器（Rate Limiter） |  |
| 5 | 1 | `problems.machines.amazon-locker` | 快递柜（Amazon Locker） |  |
| 5 | 1 | `problems.games.deck-of-cards` | 扑克牌与二十一点（Deck of Cards / Blackjack） |  |
| 5 | 0 | `problems.marketplaces.online-auction` | 在线拍卖（Online Auction） |  |
| 5 | 0 | `problems.social.linkedin` | 职业社交（LinkedIn） |  |
| 5 | 0 | `problems.social.stack-overflow` | 问答社区（Stack Overflow） |  |
| 5 | 2 | `problems.social.chat-room` | 聊天室（Chat Room） |  |
| 5 | 0 | `problems.components.task-scheduler` | 任务调度器（Task Scheduler） |  |
| 5 | 1 | `problems.components.text-editor` | 文本编辑器与撤销重做（Text Editor） |  |
| 4 | 0 | `problems.marketplaces.digital-wallet` | 数字钱包（Digital Wallet） |  |
| 4 | 0 | `problems.social.task-management` | 任务看板（Trello / Jira） |  |
| 4 | 0 | `problems.components.ttl-cache` | 带过期时间的缓存（TTL Cache） |  |
| 3 | 0 | `problems.machines.coffee-machine` | 咖啡机（Coffee Machine） |  |
| 3 | 0 | `problems.machines.traffic-signal` | 交通信号灯（Traffic Signal） |  |
| 3 | 0 | `problems.marketplaces.bank-account` | 银行账户系统（Bank Account System） |  |
| 3 | 0 | `problems.social.music-streaming` | 音乐流媒体（Spotify） |  |
| 3 | 0 | `problems.components.kv-store` | 内存键值存储（In-Memory Key-Value Store） |  |
| 1 | 0 | `problems.components.thread-pool` | 线程池（Thread Pool） |  |
| 0 | 0 | `problems.components.bounded-blocking-queue` | 有界阻塞队列（Bounded Blocking Queue） |  |

## 4. 交付物与验收

**概念层**（说明：`proposals/lld/CONCEPT_AGENT.md`）：每个叶子 4–8 张中文原生卡，代码为 Python 且能通过语法检查，不得出现 Java，带 `step`。
验收：`uv run python scripts/check_lld_concepts.py --all`

**题库**（说明：`proposals/lld/PROBLEM_AGENT.md`，任务简报：`proposals/lld/tasks/<slug>.md`），每道题：

- `problems/<slug>/solution.py`、`starter.py`、`test_*.py`：参考解必须通过测试，空模板必须失败；只用标准库，注释与文档字符串为中文
- `readings/problems/solution-<slug>.md`：中文题解，10 个固定小节，含类图；代码由 `scripts/lld_embed_code.py` 从被测文件原样嵌入
- `drills/problems/design-<slug>.md`：分关题面、怎么用 starter 练、评分点（链接到真实卡片）、题解链接
- 6–8 张中文卡，带 `step`；至少 2 条来源读物，商业网站与无许可证仓库一律 `no-archive`，付费课程的镜像不作为来源

验收：`uv run python scripts/check_lld_problems.py --all`

## 5. 台账

| 日期 | 步骤 | 结果 |
|---|---|---|
| 2026-09-20 | 调研 | 三份原始记录入库 |
| 2026-09-20 | 骨架 | 全中文重写：40 个概念叶子 + 45 个题目叶子，`validate` 0 错误 |
| 2026-09-20 | 卡片格式 | 125 张旧卡的中文段提升为正文、id 不变；中文为机翻质量，待逐张重写 |

## 6. 下一步

概念层分 4 组重写（method+oop+principles、python+structure、patterns、quality+concurrency），同时题库先做 3 道试点，再按家族每组两道题分批写；
始终保持 3 个并行代理，每批由主会话复核（跑验收、读代码、读题解、核对代理自报的疑点）后按题提交。
全部通过后：清理 Anki 里已不存在的旧卡（只删从未复习过的）、剪藏允许入库的来源、sync、validate、`anki-push` 并回读验证。

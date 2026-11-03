# LLD 学习路线

每天的流程：Anki 20 分钟，一道限时题，写完复盘 10 分钟。流程细节见 [[02-how-to-practise|怎么练]]。下一步做什么，运行 `python3 drill.py today`。

| 阶段 | 用时 | 练什么 |
|---|---|---|
| 阶段 0 · 起步 | 2 天 | 答题节奏、评分标准、练习流程 |
| 阶段 1 · 把需求变成对象 | 1 周 | 对象建模、组合优于继承、dataclass 与 Enum、Protocol 与 ABC |
| 阶段 2 · 模式与状态机 | 10 天 | 策略、观察者、状态机、命令、模式选择 |
| 阶段 3 · 基础组件 | 10 天 | 数据结构选型、时间注入、API 设计、解析与求值、错误处理 |
| 阶段 4 · 并发 | 10 天 | GIL 与竞态、锁的粒度、条件变量、生产者消费者、防超卖 |
| 阶段 5 · 业务与支付 | 10 天 | 金额与舍入、幂等、复式记账、规则引擎、事件驱动计算 |
| 阶段 6 · 模拟面试 | 1 周 | 时间管理、边写边讲、回答追问 |

## 阶段 0 · 起步（2 天）

**目标。** 知道一场 LLD 面试怎么走、怎么被打分，跑通一次完整的练习流程。

**验收。** 不看资料说出答题框架的每一步和时间分配；drill.py 的 start、test、status 都用过。

- [ ] 读答题框架和评分标准：`python3 drill.py done s0-read`
  - 打开：[[method.delivery|作答节奏]]
  - 打开：[[method.evaluation|评分标准]]
  - 打开：https://www.hellointerview.com/learn/low-level-design/in-a-hurry/introduction
  - 打开：https://www.hellointerview.com/learn/low-level-design/in-a-hurry/delivery
  - Anki：`低层设计（LLD）::01 作答方法（Machine Coding Method）`
  - Anki：`04 低层设计（Low-Level Design）::速成（In a Hurry）`
- [ ] 井字棋：第一次走完整流程，可以边写边查（40 分钟）：`python3 drill.py start tic-tac-toe -m 40`

## 阶段 1 · 把需求变成对象（1 周）

**目标。** 从一段需求里找出对象、职责和关系，用 Python 的方式写出来，不写 Java 式的继承树。

**验收。** 4 道题都在限时内全绿；能说清每个类为什么存在，以及为什么没有用继承。

- [ ] 读对象建模和设计原则：`python3 drill.py done s1-read`
  - 打开：[[method.modeling|从需求到对象]]
  - 打开：[[oop.relationships|类之间的关系]]
  - 打开：[[principles.solid|SOLID]]
  - 打开：[[principles.composition|组合优于继承]]
  - 打开：[[python.dataclasses-enums|dataclass 与 Enum]]
  - 打开：[[python.protocols-abc|Protocol、ABC 与鸭子类型]]
  - 打开：https://www.hellointerview.com/learn/low-level-design/in-a-hurry/oop-concepts
  - 打开：https://www.hellointerview.com/learn/low-level-design/in-a-hurry/design-principles
  - Anki：`低层设计（LLD）::03 对象建模（Object Modeling）`
  - Anki：`低层设计（LLD）::04 设计原则（Design Principles）`
  - Anki：`低层设计（LLD）::02 Python 对象模型与惯用法（Pythonic Design）`
- [ ] 一副牌：建模热身（40 分钟）：`python3 drill.py start deck-of-cards -m 40`
- [ ] 四子棋：棋盘、规则和胜负判断分开（45 分钟）：`python3 drill.py start connect-four -m 45`
- [ ] 海战棋：两个玩家的状态和合法性校验（45 分钟）：`python3 drill.py start battleship-game -m 45`
- [ ] 披萨订单：组合式计价（45 分钟）：`python3 drill.py start amz-pizza-order -m 45`

## 阶段 2 · 模式与状态机（10 天）

**目标。** 遇到变化点时知道该用哪个模式、什么时候不该用，并能把状态转换写得不漏分支。

**验收。** 6 道题全绿；第 2 关的改动不需要修改第 1 关已经通过的类；能说出每个模式换来了什么、付出了什么。

- [ ] 读设计模式和状态机：`python3 drill.py done s2-read`
  - 打开：[[patterns.strategy|策略]]
  - 打开：[[patterns.observer|观察者]]
  - 打开：[[patterns.state|状态]]
  - 打开：[[patterns.command|命令]]
  - 打开：[[patterns.selection|模式选择]]
  - 打开：[[structure.state-machines|状态机]]
  - 打开：https://www.hellointerview.com/learn/low-level-design/in-a-hurry/patterns
  - Anki：`低层设计（LLD）::05 设计模式（Design Patterns）`
- [ ] 售货机：状态机的基本功（50 分钟）：`python3 drill.py start vending-machine -m 50`
- [ ] 停车场：可替换的分配和计费策略（60 分钟）：`python3 drill.py start parking-lot -m 60`
- [ ] 快递柜：取件码、过期和格口分配（60 分钟）：`python3 drill.py start amazon-locker -m 60`
- [ ] 电梯：调度策略和状态转换（60 分钟）：`python3 drill.py start elevator -m 60`
- [ ] 餐厅候位：有序结构和匹配规则（45 分钟）：`python3 drill.py start restaurant-waitlist -m 45`
- [ ] 购物车折扣引擎：规则的组合和优先级（60 分钟）：`python3 drill.py start amz-discount-engine -m 60`

## 阶段 3 · 基础组件（10 天）

**目标。** 把数据结构选型讲清楚，写出边界完整、可测试的组件。这是高频 LLD 题最集中的一类。

**验收。** 10 道题全绿，其中至少 7 道不超时；每道题能说出每个操作的复杂度和用这个结构的原因。

- [ ] 读 API 设计、存储和可测试性：`python3 drill.py done s3-read`
  - 打开：[[structure.api|API 设计]]
  - 打开：[[structure.storage|存储]]
  - 打开：[[quality.testability|可测试性]]
  - 打开：[[quality.errors|错误处理]]
  - Anki：`低层设计（LLD）::08 API 与程序结构（Program Structure）`
  - Anki：`低层设计（LLD）::06 代码质量（Code Quality）`
- [ ] LRU / LFU 缓存（45 分钟）：`python3 drill.py start lru-cache -m 45`
- [ ] 带过期的缓存（45 分钟）：`python3 drill.py start ttl-cache -m 45`
- [ ] 可配置淘汰策略的键值存储（60 分钟）：`python3 drill.py start kv-store -m 60`
- [ ] 内存文件系统（60 分钟）：`python3 drill.py start in-memory-file-system -m 60`
- [ ] find 命令 API：可组合的过滤条件（50 分钟）：`python3 drill.py start amz-linux-find -m 50`
- [ ] 电子表格：依赖图和循环检测（60 分钟）：`python3 drill.py start spreadsheet-engine -m 60`
- [ ] 图片变换流水线（45 分钟）：`python3 drill.py start image-transform-pipeline -m 45`
- [ ] 限流器：多种算法同一接口（60 分钟）：`python3 drill.py start rate-limiter -m 60`
- [ ] 熔断器：状态机加时钟（50 分钟）：`python3 drill.py start api-circuit-breaker -m 50`
- [ ] 条件解析与内存表查询（60 分钟）：`python3 drill.py start query-condition-parser -m 60`

## 阶段 4 · 并发（10 天）

**目标。** 说清楚一把锁到底保护什么，能写出生产者消费者和线程池，能在预订类题里防超卖。

**验收。** 7 道题全绿且并发测试稳定；能指出每把锁保护的不变量，并说出去掉它会发生什么。

- [ ] 读并发：`python3 drill.py done s4-read`
  - 打开：[[concurrency.model|并发模型与 GIL]]
  - 打开：[[concurrency.primitives|同步原语]]
  - 打开：[[concurrency.hazards|并发风险]]
  - 打开：[[concurrency.patterns|并发模式]]
  - 打开：https://www.hellointerview.com/learn/low-level-design/concurrency/intro
  - 打开：https://www.hellointerview.com/learn/low-level-design/concurrency/correctness
  - 打开：https://www.hellointerview.com/learn/low-level-design/concurrency/coordination
  - 打开：https://www.hellointerview.com/learn/low-level-design/concurrency/scarcity
  - Anki：`低层设计（LLD）::07 并发（Concurrency）`
  - Anki：`04 低层设计（Low-Level Design）::并发（Concurrency）`
- [ ] 有界阻塞队列（40 分钟）：`python3 drill.py start bounded-blocking-queue -m 40`
- [ ] 线程池（60 分钟）：`python3 drill.py start thread-pool -m 60`
- [ ] 多线程日志框架（60 分钟）：`python3 drill.py start logger -m 60`
- [ ] 发布订阅（60 分钟）：`python3 drill.py start pub-sub -m 60`
- [ ] 任务调度器（60 分钟）：`python3 drill.py start task-scheduler -m 60`
- [ ] 电影票预订：座位锁和超时释放（60 分钟）：`python3 drill.py start movie-booking -m 60`
- [ ] 库存管理：预留、过期和防超卖（60 分钟）：`python3 drill.py start inventory-management -m 60`

## 阶段 5 · 业务与支付（10 天）

**目标。** 金额、幂等和一致性不出错。这一块和 TikTok 支付方向直接相关，也最能体现 senior 的判断。

**验收。** 9 道题全绿；金额全程不用浮点；重复请求不会重复生效，并能讲清楚为什么。

- [ ] 读 TikTok 低层设计的解答：`python3 drill.py done s5-read`
  - Anki：`02 TikTok 高频设计题::TikTok 低层设计`
  - Anki：`04 低层设计（Low-Level Design）::跨题模式（Patterns across questions）`
- [ ] 复式账本（50 分钟）：`python3 drill.py start double-entry-ledger -m 50`
- [ ] 幂等转账（50 分钟）：`python3 drill.py start idempotent-transfer -m 50`
- [ ] 额度与令牌余额（50 分钟）：`python3 drill.py start credit-token-balance -m 50`
- [ ] 计费计税引擎（60 分钟）：`python3 drill.py start billing-tax-engine -m 60`
- [ ] 配送员结算（50 分钟）：`python3 drill.py start dasher-payout -m 50`
- [ ] 数字钱包（60 分钟）：`python3 drill.py start digital-wallet -m 60`
- [ ] 分账（60 分钟）：`python3 drill.py start splitwise -m 60`
- [ ] 在线拍卖（60 分钟）：`python3 drill.py start online-auction -m 60`
- [ ] 会议调度（60 分钟）：`python3 drill.py start meeting-scheduler -m 60`

## 阶段 6 · 模拟面试（1 周）

**目标。** 用没做过的题按真实节奏走完整场，把速度和表达练稳。

**验收。** 连续 3 道没做过的题在 60 分钟内通过前 3 关，并能回答验收清单的全部问题。

- [ ] 模拟：国际象棋（60 分钟）：`python3 drill.py start chess -m 60`
- [ ] 模拟：酒店预订（60 分钟）：`python3 drill.py start hotel-booking -m 60`
- [ ] 模拟：通知服务（60 分钟）：`python3 drill.py start notification-service -m 60`
- [ ] 模拟：外卖平台（60 分钟）：`python3 drill.py start food-delivery -m 60`
- [ ] 模拟：股票经纪（60 分钟）：`python3 drill.py start stock-brokerage -m 60`
- [ ] 过一遍验收清单，没过的回到对应阶段：`python3 drill.py done s6-check`
  - 打开：[[03-readiness-checklist|验收清单]]

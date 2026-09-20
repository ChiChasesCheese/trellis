%% trellis:begin %%
# 低层设计（LLD） — study path

## Core

*30 of 85 topics: the declared Core and what it requires. Anki deals these first.*

**作答方法（Machine Coding Method）**
- [ ] [[method.delivery|作答节奏（Delivery Framework）]] — 5 cards
- [ ] [[method.evaluation|评分标准（Evaluation Rubric）]] — 5 cards
- [ ] [[method.modeling|从需求到对象（Requirements to Objects）]] — 5 cards
**Python 对象模型与惯用法（Pythonic Design）**
- [ ] [[python.data-model|数据模型与特殊方法（Data Model）]] — 6 cards
- [ ] [[python.dataclasses-enums|dataclass 与 Enum]] — 6 cards; needs: 数据模型与特殊方法（Data Model）
- [ ] [[python.protocols-abc|Protocol、ABC 与鸭子类型]] — 6 cards
- [ ] [[python.first-class-functions|一等函数、闭包与装饰器]] — 6 cards
**对象建模（Object Modeling）**
- [ ] [[oop.pillars|OOP 四大特性的实际用法]] — 5 cards
- [ ] [[oop.relationships|类之间的关系（Class Relationships）]] — 5 cards
**设计原则（Design Principles）**
- [ ] [[principles.solid|SOLID]] — 6 cards
- [ ] [[principles.composition|组合优于继承]] — 5 cards; needs: 类之间的关系（Class Relationships）
**设计模式（Design Patterns）**
- [ ] [[patterns.strategy|策略模式与可替换算法（Strategy）]] — 6 cards; needs: 一等函数、闭包与装饰器
- [ ] [[patterns.observer|观察者与事件（Observer）]] — 6 cards
- [ ] [[patterns.state|状态模式（State）]] — 6 cards; needs: dataclass 与 Enum
- [ ] [[patterns.command|命令与撤销重做（Command）]] — 6 cards
**并发（Concurrency）**
- [ ] [[concurrency.model|线程、GIL 与内存模型]] — 6 cards
- [ ] [[concurrency.primitives|同步原语（threading）]] — 5 cards; needs: 线程、GIL 与内存模型
**API 与程序结构（Program Structure）**
- [ ] [[structure.api|进程内 API 设计]] — 4 cards
- [ ] [[structure.state-machines|状态机（State Machines）]] — 5 cards; needs: 状态模式（State）
- [ ] [[structure.storage|内存持久化（In-Memory Persistence）]] — 4 cards
**设计题（Design Problems）**
- [ ] [[problems.machines.parking-lot|停车场（Parking Lot）]] — 8 cards; needs: 策略模式与可替换算法（Strategy）, 内存持久化（In-Memory Persistence）
- [ ] [[problems.machines.elevator|电梯系统（Elevator System）]] — 8 cards; needs: 状态机（State Machines）, 策略模式与可替换算法（Strategy）
- [ ] [[problems.machines.vending-machine|自动售货机（Vending Machine）]] — 8 cards; needs: 状态模式（State）
- [ ] [[problems.booking.movie-booking|电影订票（BookMyShow）]] — 8 cards; needs: 内存持久化（In-Memory Persistence）, 同步原语（threading）
- [ ] [[problems.games.chess|国际象棋（Chess）]] — 8 cards; needs: OOP 四大特性的实际用法, 命令与撤销重做（Command）
- [ ] [[problems.marketplaces.splitwise|分账（Splitwise）]] — 9 cards; needs: 策略模式与可替换算法（Strategy）
- [ ] [[problems.marketplaces.online-shopping|在线购物（Amazon）]] — 9 cards; needs: 状态机（State Machines）, 内存持久化（In-Memory Persistence）
- [ ] [[problems.marketplaces.ride-sharing|网约车（Uber）]] — 8 cards; needs: 策略模式与可替换算法（Strategy）, 状态机（State Machines）
- [ ] [[problems.social.social-network|社交网络（Social Network）]] — 8 cards; needs: 观察者与事件（Observer）
- [ ] [[problems.components.lru-cache|LRU / LFU 缓存]] — 8 cards; needs: 数据模型与特殊方法（Data Model）, 进程内 API 设计
## The rest

**作答方法（Machine Coding Method）**
- [ ] [[method.diagrams|白板上的 UML（Class & Sequence Diagrams）]] — 5 cards; needs: 从需求到对象（Requirements to Objects）
**Python 对象模型与惯用法（Pythonic Design）**
- [ ] [[python.context-iterators|上下文管理器、迭代器与生成器]] — 6 cards
- [ ] [[python.typing|类型注解作为设计工具]] — 6 cards; needs: Protocol、ABC 与鸭子类型
- [ ] [[python.modules|模块、包与依赖方向]] — 6 cards
**对象建模（Object Modeling）**
- [ ] [[oop.interfaces|接口与抽象基类]] — 5 cards; needs: Protocol、ABC 与鸭子类型
- [ ] [[oop.values|值对象与不可变性（Value Objects）]] — 5 cards; needs: dataclass 与 Enum
**设计原则（Design Principles）**
- [ ] [[principles.coupling|耦合、内聚与依赖注入]] — 5 cards
- [ ] [[principles.simplicity|DRY、KISS、YAGNI]] — 5 cards
**设计模式（Design Patterns）**
- [ ] [[patterns.creational|创建型模式（Creational）]] — 6 cards
- [ ] [[patterns.structural|结构型模式（Structural）]] — 7 cards
- [ ] [[patterns.behavioral|其余行为型模式（Behavioral）]] — 7 cards
- [ ] [[patterns.selection|选择与拒绝模式]] — 6 cards; needs: DRY、KISS、YAGNI
**代码质量（Code Quality）**
- [ ] [[quality.smells|代码坏味道（Code Smells）]] — 6 cards
- [ ] [[quality.refactoring|核心重构手法]] — 4 cards
- [ ] [[quality.testability|为测试而设计]] — 4 cards; needs: 耦合、内聚与依赖注入
- [ ] [[quality.fitness-functions|适应度函数（Fitness Functions）]] — 4 cards; needs: 为测试而设计
- [ ] [[quality.errors|错误处理设计]] — 6 cards
**并发（Concurrency）**
- [ ] [[concurrency.hazards|死锁及其亲戚]] — 6 cards; needs: 同步原语（threading）
- [ ] [[concurrency.patterns|并发模式]] — 7 cards; needs: 同步原语（threading）
- [ ] [[concurrency.asyncio|asyncio 与协程]] — 6 cards; needs: 线程、GIL 与内存模型
**设计题（Design Problems）**
- [ ] [[problems.machines.atm|ATM 取款机]] — 12 cards; needs: 状态模式（State）
- [ ] [[problems.machines.amazon-locker|快递柜（Amazon Locker）]] — 8 cards; needs: 内存持久化（In-Memory Persistence）
- [ ] [[problems.machines.coffee-machine|咖啡机（Coffee Machine）]] — 13 cards; needs: 同步原语（threading）
- [ ] [[problems.machines.traffic-signal|交通信号灯（Traffic Signal）]] — 8 cards; needs: 状态机（State Machines）
- [ ] [[problems.booking.hotel-booking|酒店预订（Hotel Booking）]] — 8 cards; needs: 状态机（State Machines）
- [ ] [[problems.booking.car-rental|租车系统（Car Rental）]] — 8 cards; needs: 策略模式与可替换算法（Strategy）
- [ ] [[problems.booking.library|图书馆管理（Library Management）]] — 8 cards; needs: 类之间的关系（Class Relationships）
- [ ] [[problems.booking.airline|航班管理（Airline Management）]] — 8 cards; needs: 状态机（State Machines）
- [ ] [[problems.booking.meeting-scheduler|会议室预订（Meeting Scheduler）]] — 8 cards; needs: 内存持久化（In-Memory Persistence）
- [ ] [[problems.booking.restaurant|餐厅管理（Restaurant Management）]] — 9 cards; needs: 状态机（State Machines）
- [ ] [[problems.games.tic-tac-toe|井字棋（Tic-Tac-Toe）]] — 8 cards; needs: 从需求到对象（Requirements to Objects）
- [ ] [[problems.games.snake-and-ladder|蛇梯棋（Snake and Ladder）]] — 9 cards; needs: 策略模式与可替换算法（Strategy）
- [ ] [[problems.games.cricinfo|体育比分系统（Cricinfo）]] — 8 cards; needs: 观察者与事件（Observer）
- [ ] [[problems.games.deck-of-cards|扑克牌与二十一点（Deck of Cards / Blackjack）]] — 9 cards; needs: dataclass 与 Enum
- [ ] [[problems.marketplaces.stock-brokerage|股票交易系统（Stock Brokerage）]] — 8 cards; needs: 内存持久化（In-Memory Persistence）
- [ ] [[problems.marketplaces.food-delivery|外卖配送（Food Delivery）]] — 8 cards; needs: 状态机（State Machines）
- [ ] [[problems.marketplaces.online-auction|在线拍卖（Online Auction）]] — 8 cards; needs: 同步原语（threading）
- [ ] [[problems.marketplaces.digital-wallet|数字钱包（Digital Wallet）]] — 8 cards; needs: 死锁及其亲戚
- [ ] [[problems.marketplaces.bank-account|银行账户系统（Bank Account System）]] — 8 cards; needs: 内存持久化（In-Memory Persistence）
- [ ] [[problems.social.linkedin|职业社交（LinkedIn）]] — 8 cards; needs: 类之间的关系（Class Relationships）
- [ ] [[problems.social.stack-overflow|问答社区（Stack Overflow）]] — 8 cards; needs: 类之间的关系（Class Relationships）
- [ ] [[problems.social.chat-room|聊天室（Chat Room）]] — 8 cards; needs: 观察者与事件（Observer）
- [ ] [[problems.social.task-management|任务看板（Trello / Jira）]] — 8 cards; needs: 状态机（State Machines）
- [ ] [[problems.social.music-streaming|音乐流媒体（Spotify）]] — 8 cards; needs: 状态模式（State）
- [ ] [[problems.components.logger|日志框架（Logging Framework）]] — 9 cards; needs: 观察者与事件（Observer）, 结构型模式（Structural）
- [ ] [[problems.components.in-memory-file-system|内存文件系统（In-Memory File System）]] — 8 cards; needs: 结构型模式（Structural）
- [ ] [[problems.components.notification-service|通知服务（Notification Service）]] — 10 cards; needs: 策略模式与可替换算法（Strategy）, 观察者与事件（Observer）
- [ ] [[problems.components.pub-sub|发布订阅与事件总线（Pub-Sub）]] — 10 cards; needs: 观察者与事件（Observer）, 并发模式
- [ ] [[problems.components.rate-limiter|限流器（Rate Limiter）]] — 8 cards; needs: 策略模式与可替换算法（Strategy）, 同步原语（threading）
- [ ] [[problems.components.task-scheduler|任务调度器（Task Scheduler）]] — 8 cards; needs: 并发模式
- [ ] [[problems.components.text-editor|文本编辑器与撤销重做（Text Editor）]] — 10 cards; needs: 命令与撤销重做（Command）
- [ ] [[problems.components.ttl-cache|带过期时间的缓存（TTL Cache）]] — 8 cards; needs: 进程内 API 设计
- [ ] [[problems.components.kv-store|内存键值存储（In-Memory Key-Value Store）]] — 8 cards; needs: 内存持久化（In-Memory Persistence）
- [ ] [[problems.components.thread-pool|线程池（Thread Pool）]] — 8 cards; needs: 并发模式
- [ ] [[problems.components.bounded-blocking-queue|有界阻塞队列（Bounded Blocking Queue）]] — 8 cards; needs: 同步原语（threading）
%% trellis:end %%

## Notes

# OOD 题单（Object-Oriented Design）

每一篇是一道完整的 OOD 题：题目在考什么、开场先问什么、核心对象和类图、主流程、关键决策（结论加粗）、一份能跑的
Python 骨架、面试官加需求时改哪里、并发与扩展、常见错误，最后是 30 秒复述。每篇 20 分钟内读完；**先读文章，骨架有时间再敲**。

## 怎么读

- 先读 [[ood00-round-framework]]：45 分钟怎么分配、评分看什么、加需求时怎么回答——后面每一篇都按这个框架走。
- 然后按下表顺序读。每读完一篇，合上它，把「30 秒复述」说出口；说不出来的那一条回去重看「关键决策」。
- 时间不够时：只读第一张表；每篇只看「核心对象」「关键决策」「面试官加需求时」「30 秒复述」四节，约 8 分钟。
- 想刷题：把「Python 骨架」的方法体删掉，30 分钟内重写到 demo 的 `assert` 全部通过。

## Amazon 最近考到的

| # | 题 | 考什么 |
|---|---|---|
| 00 | [[ood00-round-framework\|作答框架]] | 45 分钟节奏、评分维度、加需求的回答方式 |
| 01 | [[ood01-file-search\|Linux find / 文件搜索]] | 过滤条件做成可组合的对象（AND / OR），新增条件只加一个类 |
| 02 | [[ood02-amazon-locker\|快递柜]] | 最小可容纳分配、取件码不是密码、过期回收、并发分配 |
| 03 | [[ood03-checkout-discount\|购物车折扣引擎]] | 折扣规则可插拔、行级与整单折扣分层、钱用整数分 |
| 04 | [[ood04-pizza-order\|披萨订单]] | 菜单是数据不是类、Builder 校验组合、复用折扣规则 |
| 05 | [[ood05-train-fare\|火车线路票价]] | 前缀和算票价、动态加站、周末封顶这类规则怎么插进来 |
| 06 | [[ood06-parking-lot\|停车场与计费]] | 车位分配、按时段切段计费、时间从外部注入 |
| 07 | [[ood07-configurable-cache\|可配置缓存（LRU / LFU）]] | 淘汰策略与存储后端两条独立变化的轴：组合而不是继承 |
| 08 | [[ood08-pubsub\|发布订阅]] | 一个订阅者出错不拖累其他人、主题过滤、慢订阅者 |
| 09 | [[ood09-dag-runner\|DAG 执行器与依赖安装]] | 拓扑排序与环检测、代码评审找 bug、并行执行与失败传播 |
| 10 | [[ood10-closest-store\|增删查最近值]] | 前驱 / 后继两个候选、有序列表与按值域分桶的取舍 |
| 11 | [[ood11-robot-restaurant\|机器人餐厅]] | 机器人状态机、忙闲调度、电量不足 |
| 12 | [[ood12-file-watcher\|文件监听器]] | 快照比对、回调线程与停止、去抖 |
| 13 | [[ood13-in-memory-db\|内存数据库]] | 表与增删改查、WHERE / ORDER BY / JOIN、小 SQL 解析器 |

## Amazon 考过、但不在最近一个月（low priority）

| # | 题 | 考什么 |
|---|---|---|
| 14 | [[ood14-rate-limiter\|限流器]] | 固定窗口 / 滑动窗口 / 令牌桶的取舍、按用户隔离、分布式 |
| 15 | [[ood15-logger\|日志框架]] | 格式化与输出分离、按级别分发、慢输出不阻塞业务 |
| 16 | [[ood16-splitwise\|分账]] | 分摊方式做成策略、零头怎么分、债务化简 |
| 17 | [[ood17-task-scheduler\|任务调度器]] | 延时与周期任务、堆 + 条件变量、取消 |
| 18 | [[ood18-aws-billing\|AWS 账单服务]] | 阶梯价是边际的、先聚合再计价、用量去重 |
| 19 | [[ood19-occupancy-tracker\|办公室人数追踪]] | 事件溯源、前缀和 + 二分查任意时刻人数 |
| 20 | [[ood20-wallet\|钱包与银行账户]] | 余额由流水推出、转账原子性、费用规则 |
| 21 | [[ood21-dns-resolver\|DNS 解析器与 TTL 缓存]] | TTL 过期、上游健康检查与切换、读多写少 |
| 22 | [[ood22-music-playlist\|音乐播放与播放列表]] | 播放队列、随机与重复模式、推荐做成可替换策略 |
| 23 | [[ood23-video-catalogue\|视频目录与续播]] | 目录索引、按用户记录观看位置、跨设备续播 |

## 经典高频题（low priority）

| # | 题 | # | 题 |
|---|---|---|---|
| 24 | [[ood24-elevator\|电梯系统]] | 40 | [[ood40-car-rental\|租车系统]] |
| 25 | [[ood25-vending-machine\|自动售货机]] | 41 | [[ood41-coffee-machine\|咖啡机]] |
| 26 | [[ood26-atm\|ATM 取款机]] | 42 | [[ood42-traffic-signal\|交通信号灯]] |
| 27 | [[ood27-movie-booking\|电影订票]] | 43 | [[ood43-kv-store\|内存键值存储]] |
| 28 | [[ood28-hotel-booking\|酒店预订]] | 44 | [[ood44-in-memory-file-system\|内存文件系统]] |
| 29 | [[ood29-library\|图书馆管理]] | 45 | [[ood45-social-network\|社交网络]] |
| 30 | [[ood30-tic-tac-toe\|井字棋]] | 46 | [[ood46-linkedin\|职业社交]] |
| 31 | [[ood31-chess\|国际象棋]] | 47 | [[ood47-stack-overflow\|问答社区]] |
| 32 | [[ood32-snake-and-ladder\|蛇梯棋]] | 48 | [[ood48-chat-room\|聊天室]] |
| 33 | [[ood33-online-shopping\|在线购物]] | 49 | [[ood49-airline\|航班管理]] |
| 34 | [[ood34-ride-sharing\|网约车]] | 50 | [[ood50-cricinfo\|体育比分系统]] |
| 35 | [[ood35-food-delivery\|外卖平台]] | 51 | [[ood51-deck-of-cards\|扑克牌]] |
| 36 | [[ood36-stock-brokerage\|股票交易系统]] | 52 | [[ood52-online-auction\|在线拍卖]] |
| 37 | [[ood37-notification-service\|通知服务]] | 53 | [[ood53-thread-pool\|线程池]] |
| 38 | [[ood38-meeting-scheduler\|会议室预订]] | 54 | [[ood54-bounded-blocking-queue\|有界阻塞队列]] |
| 39 | [[ood39-text-editor\|文本编辑器与撤销重做]] | 55 | [[ood55-task-management\|任务管理（看板）]] |

想看更完整的推导、测试和分关练习：每题的长版题解在低层设计域（`solution-*`），Anki 在 `低层设计（LLD）::10 Amazon 专项`。

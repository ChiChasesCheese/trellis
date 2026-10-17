You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
Amazon 专项（Amazon OOD） › 钱包与账户（Wallet / Bank Account）（low priority）
存取款、转账、对账与税费：金额不可变、余额由流水推出、可扩展的费用规则。

## Position in the knowledge map
Prerequisites (assume known):
  - 数字钱包（Digital Wallet）: 充值、转账、交易记录，余额不能为负且转账两边一致。
Sibling topics (OUT of scope):
  - Amazon 的 LLD 轮怎么打（Amazon OOD Round）: 45 分钟、LP 开场、记事本写可编译但不运行的代码、追加 5–6 条需求；评分是「Logical and Maintainable」。
  - 增删查最近值（Add / Remove / Closest）: 电面 OOD：维护一组数，支持插入、删除、查询离 target 最近的数；从排序列表到值域分桶。
  - 火车线路票价（Train Fare Calculator）: G→U→H→K→I 相邻站一元，calculateFare(start, stop)，动态加站，周末封顶。
  - 购物车折扣引擎（Checkout Price Engine）: 折扣基类 isEligible / apply，百分比、满减、买 X 送 Y 叠加；钱用整数分；规则可插拔。
  - 披萨订单（Pizza Order）: 饼底、尺寸、配料自由组合并算总价：菜单是数据不是类，Builder 校验组合，复用折扣规则。
  - Linux find 命令 API（File Search API）: 按大小、后缀、名字过滤文件，AND / OR 组合，新增条件只加一个类；符号链接环与惰性遍历。
  - 应急事件发布订阅（Emergency Pub/Sub）: 组件订阅 / 发布应急事件；一个订阅者失败不拖累其他人，主题过滤、优先级与重试。
  - 可配置缓存（Configurable Cache）: 淘汰策略（LRU / LFU）与存储后端（内存、文件）可互换：两条独立变化的轴。
  - 停车场计费（Parking Lot Fees）: 停车场的重点放在计费：按车型、时段、封顶、会员等不同规则，规则可组合、时间可注入。
  - Amazon 现场版快递柜（Amazon Locker, onsite）: SDE II 现场原题：在题库快递柜之上，Amazon 面试官会追问什么、45 分钟写到哪一步。
  - 机器人餐厅（Robot Restaurant）: 电面 OOD：点单、机器人分配、做菜与送餐状态机，机器人忙闲调度。
  - 文件监听器（File Watcher）: 监听目录的创建 / 修改 / 删除并回调：快照比对、去抖、递归目录、回调线程与关闭。
  - DAG 执行器与依赖安装（DAG Runner）: 依赖安装顺序与环检测，Step Function 式 DAG 执行顺序的 code review 找 bug，再到并行执行与失败传播。
  - 内存数据库（In-Memory Database）: 建表与增删改查，再到 WHERE / ORDER BY / JOIN、一个小 SQL 解析器、索引与事务：一道题走完数据库的骨架。
  - AWS 账单服务（AWS Billing Service）（low priority）: 按用量计费：阶梯价、免费额度、按服务汇总、用量记录去重，钱用整数分。
  - 办公室人数追踪（Occupancy Tracker）（low priority）: 刷卡进出事件，查询任意时刻楼里有多少人：事件溯源、前缀和加二分、同一模型的 SQL 写法。
  - 限流器（Rate Limiter）（low priority）: 在题库限流器之上：Amazon 追问的窗口算法取舍、按用户隔离、分布式时的一致性与租约。
  - 日志框架（Logger）（low priority）: 在题库日志框架之上：多种消息格式、按级别与目的地分发、慢写入不阻塞业务。
  - 分账（Splitwise）（low priority）: 在题库分账之上：均分 / 按比例 / 按份额，零头怎么分，债务化简。
  - 任务调度器（Task Scheduler）（low priority）: 在题库任务调度器之上：延时与周期任务、取消、线程与阻塞的追问。
  - 播放列表与推荐（Playlist DJ）（low priority）: 混音播放列表加推荐服务：需求一次列十条时怎么拆类、怎么排优先级。
  - DNS 解析器（DNS Resolver）（low priority）: 带 TTL 的缓存、上游健康检查与切换、读多写少的快速查询。
  - 视频目录与续播（Video Catalogue）（low priority）: 影片目录、分类浏览、暂停时记录观看位置并跨设备续播。

## Rules
- Write 6 cards for THIS topic only. Sibling topics listed above are
  out of scope — never restate their material.
- One card = one retrievable fact, mechanism, trade-off, or number. If an
  answer needs more than ~4 sentences, split the card.
- Prefer questions that force discrimination ("when would you choose X
  over Y") over definitions, except for terms of art.
- Use `type: "cloze"` with {{c1::...}} syntax for formulas, sequences,
  and lists; `type: "qa"` otherwise.
- Markdown allowed in q/a/text (code spans, tables, lists).
- id: lowercase-hyphenated slug, unique, descriptive, stable.

## Output format (JSON array only, no prose)
[
  {"id": "example-qa-card", "node": "amazon.amz-wallet", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "amazon.amz-wallet", "type": "cloze",
    "text": "The formula is {{c1::W + R > N}}.", "tags": []}
]

## Language and self-containment
- Write every card in Chinese (简体中文). Terms of art stay in English (the reader will
  meet them in code, configs and docs): write the English term and gloss
  it in Chinese (简体中文) once per card, e.g. `consumer group（消费者群组）`.
- SELF-CONTAINED. A reader who has never heard of 低层设计（LLD） must understand
  the card from the card alone: the question carries the situation it is
  asking about, the answer defines every term it uses and says WHY, not
  only what. Never "as discussed", "the book says", "see chapter 3" — nor
  their equivalents ("书中建议", "本书", "如前所述"): the importer refuses a
  card that leans on its source. State the advice as a fact.
- Prefer questions whose answer is a mechanism or a decision ("what happens
  when…", "why would you set…") over ones whose answer is a name.
- Do not set `source`; the importer records where these cards came from.

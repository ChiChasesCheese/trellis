You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
Amazon 专项（Amazon OOD） › Linux find 命令 API（File Search API）
按大小、后缀、名字过滤文件，AND / OR 组合，新增条件只加一个类；符号链接环与惰性遍历。

## Position in the knowledge map
Prerequisites (assume known):
  - 结构型模式（Structural）: 适配器、装饰器（与 `@decorator` 的区别）、外观、组合、代理、桥接、享元。
  - 接口与抽象基类: 面向接口编程；接口与抽象类的取舍；在 Python 里落到 Protocol 还是 ABC。
Sibling topics (OUT of scope):
  - Amazon 的 LLD 轮怎么打（Amazon OOD Round）: 45 分钟、LP 开场、记事本写可编译但不运行的代码、追加 5–6 条需求；评分是「Logical and Maintainable」。
  - 增删查最近值（Add / Remove / Closest）: 电面 OOD：维护一组数，支持插入、删除、查询离 target 最近的数；从排序列表到值域分桶。（重建）
  - 火车线路票价（Train Fare Calculator）: G→U→H→K→I 相邻站一元，calculateFare(start, stop)，动态加站，周末封顶。
  - 购物车折扣引擎（Checkout Price Engine）: 折扣基类 isEligible / apply，百分比、满减、买 X 送 Y 叠加；钱用整数分；规则可插拔。
  - 应急事件发布订阅（Emergency Pub/Sub）: 组件订阅 / 发布应急事件；一个订阅者失败不拖累其他人，主题过滤、优先级与重试。
  - 可配置缓存（Configurable Cache）: 淘汰策略（LRU / LFU）与存储后端（内存、文件）可互换：两条独立变化的轴。
  - 停车场计费（Parking Lot Fees）: 停车场的重点放在计费：按车型、时段、封顶、会员等不同规则，规则可组合、时间可注入。
  - Amazon 现场版快递柜（Amazon Locker, onsite）: SDE II 现场原题：在题库快递柜之上，Amazon 面试官会追问什么、45 分钟写到哪一步。
  - 机器人餐厅（Robot Restaurant）: 电面 OOD：点单、机器人分配、做菜与送餐状态机，机器人忙闲调度。（重建）
  - 文件监听器（File Watcher）: 监听目录的创建 / 修改 / 删除并回调：快照比对、去抖、递归目录、回调线程与关闭。（重建）
  - DAG 执行器与依赖安装（DAG Runner）: 依赖安装顺序与环检测，Step Function 式 DAG 执行顺序的 code review 找 bug，再到并行执行与失败传播。

## Rules
- Write 8 cards for THIS topic only. Sibling topics listed above are
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
  {"id": "example-qa-card", "node": "amazon.amz-linux-find", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "amazon.amz-linux-find", "type": "cloze",
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

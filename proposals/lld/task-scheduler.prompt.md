You are writing spaced-repetition flashcards for the topic below. Follow
every rule; output only the JSON.

## Topic
设计题（Design Problems） › 基础组件 › 任务调度器（Task Scheduler）
延时与周期任务：堆加条件变量的调度线程、取消与工作线程池。

## Position in the knowledge map
Prerequisites (assume known):
  - 并发模式: 生产者-消费者、有界阻塞队列、线程池与 `concurrent.futures`、读写锁、安全的惰性初始化。
Sibling topics (OUT of scope):
  - LRU / LFU 缓存: O(1) 的 get/put：哈希表加双向链表，LFU 变体，线程安全版本。
  - 日志框架（Logging Framework）: 级别过滤、多输出目的地、格式化器，异步写入与线程安全。
  - 内存文件系统（In-Memory File System）: 目录树的组合模式、路径解析、mkdir/ls/read/write 与搜索。
  - 通知服务（Notification Service）: 多渠道发送、用户偏好、模板与重试——进程内版本。
  - 发布订阅与事件总线（Pub-Sub）: 主题、订阅者、消息分发与位点，线程安全的进程内消息队列。
  - 限流器（Rate Limiter）: 令牌桶、滑动窗口的类设计，可注入时钟，按用户隔离与线程安全。
  - 文本编辑器与撤销重做（Text Editor）: 插入/删除/光标操作，命令模式实现的撤销重做。
  - 带过期时间的缓存（TTL Cache）: 惰性过期与主动清理、可注入时钟、与淘汰策略组合。
  - 内存键值存储（In-Memory Key-Value Store）: 分关递进的机考题型：基本读写 → 扫描与前缀 → TTL → 事务或备份恢复。
  - 线程池（Thread Pool）: 工作线程、任务队列、Future 结果、优雅关闭与拒绝策略。
  - 有界阻塞队列（Bounded Blocking Queue）: 用 Condition 实现的生产者-消费者：满则阻塞、空则等待、超时与关闭。

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
  {"id": "example-qa-card", "node": "problems.components.task-scheduler", "type": "qa",
    "q": "Question?", "a": "Answer.", "tags": []},
  {"id": "example-cloze-card", "node": "problems.components.task-scheduler", "type": "cloze",
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

---
nodes: [problems.components.pub-sub, patterns.observer, concurrency.patterns]
tags: [problem]
---
# Drill：发布订阅与事件总线（Pub-Sub）

一个**进程内**的消息总线：发布者把消息投到某个主题，订阅者订阅自己关心的主题。规模是几十个
主题、几十个订阅者、每秒几千条消息，全部在一个 Python 进程里，没有网络也没有落盘。八行的
`dict[str, list[callback]]` 版本谁都写得出，这道题的分数全在面试官的下一句话上——**"如果其中一个
订阅者处理得特别慢呢？"**。照真实机考的节奏分关来做，做完一关再看下一关。时间一律来自注入的
时钟，代码里不许出现 `time.time()`。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：主题、发布、订阅、退订。消息要送到该主题**所有**订阅者手上。两条最容易
  被跳过的要求必须做到并各写一个用例：一个订阅者的处理函数抛异常，**不许影响其他订阅者**，
  也**不许影响它自己后面的消息**（它的位点照样前进）。退订之后不再收到消息。
- 第 2 关（约 10 分钟）：把投递模型的选择摆上台面——推（订阅者给回调）还是拉（主题保留一条
  日志、订阅者各持一个位点）。两边各说一句代价，挑一个实现，并说清另一个买到了什么。选拉的话
  必须把**重放**（把位点移回去重读同一批消息）和**迟到订阅者能看到历史**这两件事写出来并测到。
- 第 3 关（约 12 分钟）：保留日志有容量上限，写出你的**溢出策略**并说明为什么选它（丢最旧／
  阻塞发布者／拒绝发布）。给推模式加投递线程，然后把顺序保证**精确地**写下来：同一主题对同一
  订阅者按发布顺序，跨主题和跨订阅者不保证。测试这样写：4 条发布线程用栅栏同时起跑各发 50 条，
  全部结束后关闭总线，断言恰好收到 200 条、位点严格递增无重复、每个发布者自己那 50 条的相对
  顺序也保住。再写一个相反的：容量设成 3、发 6 条，断言日志长度仍是 3 **且掉队条数被计了出来**。
- 第 4 关（选做）：通配订阅（`orders.*` 吃一段、`orders.#` 吃余下所有段）与死信主题。判分点只有
  一个：加这两样东西，前三关的追加、读取、投递三个方法是不是一行都不用改。顺带回答：订了 `#`
  的消费者会不会把自己产生的死信再吃一遍？

**怎么练**：把 `vault/domains/low-level-design/problems/pub-sub/starter.py` 的方法体补全，然后在
仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/pub-sub -q`。

**评分点**
- 开口第一句就把范围钉死："这是进程内的事件总线，不是分布式消息系统"，Kafka 只作为对照出现。
- 投递模型讲成一次**有代价的选择**而不是默认动作，说得出拉买到了重放与慢订阅者隔离（[[problems-pub-sub-push-vs-pull]]）。
- 位点归主题管、和日志同一把锁，说得出"最慢位点"这个查询为什么决定了归属（[[problems-pub-sub-cursor-owned-by-topic]]）。
- 日志有容量上限，三种溢出策略各说得出代价，默认选丢最旧并给理由（[[problems-pub-sub-overflow-policy-three]]）。
- 阻塞策略等待的是"最慢位点越过队头"，不是"日志变短"；拒绝策略共用同一判据（[[problems-pub-sub-eviction-condition]]）。
- 丢弃一定被计数并暴露成公开属性，绝不静默丢数据（[[problems-pub-sub-shared-log-vs-per-subscriber-queue]]）。
- 顺序保证精确到"每主题每订阅者"，并用栅栏加真线程测出来，而不是靠 sleep（[[problems-pub-sub-ordering-guarantee-scope]]、[[concurrency-producer-consumer-queue]]）。
- 订阅者抛出的异常被投递线程吞掉并计数，失败策略是一个函数而不是抽象基类（[[problems-pub-sub-failing-subscriber-isolation]]、[[patterns-observer-partial-failure]]）。
- 退订做满"摘注册表 → 排空 → join → 摘位点"四步，退订后 `cursor_count` 归零（[[problems-pub-sub-unsubscribe-releases-cursor]]）。
- 死信主题就是一个普通主题；通配不匹配 `$` 开头的内部主题，否则失败一次就成死循环（[[problems-pub-sub-dead-letter-is-a-topic]]）。
- 总线是普通类，不用 `__new__` 单例；需要全局实例就放一个模块级对象（[[problems-pub-sub-no-new-singleton]]）。
- 回调订阅者时**不持任何锁**，消息是冻结的事件对象，订阅者不回头读主题的状态（[[patterns-observer-notify-lock]]）。

**题解**：[[solution-pub-sub]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

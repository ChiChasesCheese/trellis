---
nodes: [problems.booking.library, oop.relationships]
tags: [problem]
---
# Drill：图书馆管理（Library Management）

一座中型图书馆：几万个书目、每个书目一到几册实体馆藏、几千名读者分学生／教师／公众三类。
读者搜书、借书、还书、续借；没书时可以预约排队，还回来通知队首的人来取。这是面向对象设计里
被讲烂了的一道题，所以考法已经变了：面试官想看的不是你能不能写出三个类，而是**你在一道熟题上
能不能比模板答案多说出点什么**。动手之前先回答一句：「一本书」到底指什么？

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：目录、借出、归还。第一件事是把**书目**（一部作品的著录记录）和
  **馆藏副本**（贴着条码的那一册）分开，并说清搜索、借还、预约这三件事各挂在哪一个上。
  检索写成子串扫描就够——顺便说出**为什么这道题里检索是送分项**。
- 第 2 关（约 15 分钟）：按读者类型的借阅上限与借期；续借（有次数上限）；逾期罚金。
  罚金要能在读者**还没还书**的时候就答出「现在欠多少」——这条要求直接决定它是存字段还是算出来。
  时钟必须注入，代码里不许出现 `sleep`。
- 第 3 关（约 15 分钟）：预约队列。先来先到、还回来给队首、留在取书架上等他来取。
  写之前先把三个问题答完：**书还回来给谁？留多久？他不来取怎么办？**然后回答一个自检题：
  一位读者离开队列一共有几条路径？每一条你都让队列缩了吗？
- 第 4 关（选做）：加一种介质（DVD 借 2 天、罚金翻四倍、取书架只留 1 天）或一种读者类型；
  再加上并发——十个人同时借一个有三册的书目。判分点只有两个：加介质、加读者类型**只加一行政策**，
  借还流程一行不动；并发测试断言的是不变量（恰好三笔，且**三个条码互不相同**），不是时序。

**怎么练**：把 `vault/domains/low-level-design/problems/library/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/library -q`。

**评分点**
- 书目与副本分开，并说得出搜索挂书目、借还挂副本、预约排书目的队、取书架上留的是那一本副本
  （[[problems-library-title-vs-copy]]、[[oop-entity-vs-value-object]]）。
- 拒绝为图书／DVD／期刊建继承树，说得出 `get_author_or_publisher()` 是命名问题而不是多态问题
  （[[problems-library-no-item-subclasses]]）。
- 「谁拿到哪一本」只有一份规则，在读写入口惰性触发；没有定时器、没有后台线程，因此完全可测
  （[[problems-library-sweep-is-the-only-allocator]]）。
- 取书架上的保留有到期时刻，到期即下架；并且答得出「过期的人回队尾还是出局」以及为什么
  （[[problems-library-hold-shelf-must-expire]]）。
- 有人排队时拒绝续借，并说得出判据（承诺优先于方便）；续借次数有上限、到期日从今天起算
  （[[problems-library-renewal-yields-to-the-queue]]）。
- 罚金是按当前时刻算出来的，书还着按现在算、还了冻结在归还时刻；时钟注入，金额用整数分
  （[[problems-library-fine-is-computed]]）。
- 借期、限额、罚金费率、留架天数来自一张按 (读者类型, 介质) 查的政策表，不是继承树也不是
  `if` 分支（[[problems-library-policy-table-not-inheritance]]、[[patterns-strategy-callable]]）。
- 并发测试用 `Barrier` 对齐起跑，断言「三笔」**且**「三个条码互不相同」，并说得出 GIL 给了什么、
  没给什么（[[problems-library-concurrent-lend-assert]]）。
- 检索保持朴素并说明理由；拒绝一组 `SearchByXxxStrategy` 类、拒绝一个状态一个状态类、
  拒绝 `get_instance()` 单例（[[patterns-strategy-misuse]]）。
- 对外只给不可变快照（`tuple` / `frozenset`），从不把内部的 `list` 或 `dict` 交出去
  （[[oop-getter-collection-leak]]）。

**题解**：[[solution-library]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

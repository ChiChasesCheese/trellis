---
nodes: [lcproject.lcp-feature-flag, patterns.strategy, concurrency-depth.compound-actions]
tags: [problem]
---
# Drill：功能开关与实验分组（Feature Flag）

一个产品团队用功能开关逐步放量新功能、做 A/B 实验：每个开关有一组变体、一串按顺序匹配的定向规则，规则之外的用户按百分比稳定分组。
服务在内存里存配置，被多个线程同时读写，对外是创建、读取、更新、删除、列出和求值六个方法。计划用时 60 分钟，最后留出时间写三篇关于分桶、更新原子性和多实例的短文。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的十三条规则逐条改写成断言。然后做创建、读取、列出、删除与校验：
  放量表必须是整数、非负、总和 100，key 要整串匹配正则，正文 key 与路径 key 不一致抛 `ValidationError`；多余属性被丢掉，返回值随便改也不影响存储。
- 第 2 关（约 15 分钟）：求值的规则部分。停用返回 `default_variant`；规则自上而下，首个全部命中的赢，返回 `rule_index`；七个操作符，
  属性缺失或类型不符一律为 False 且不抛异常，`true` 不等于 `1`，`10**23` 不等于 `1e23`。
- 第 3 关（约 15 分钟）：分桶。按合同公式算桶号，`acct-1` 得 468，`acct-42` 得 8016；区间按 `variants` 顺序累计、左闭右开；
  把 80/20 改成 70/30 之后，原来在 candidate 里的用户一个都不能少。
- 第 4 关（约 15 分钟）：三十二个线程同时创建同名开关恰好一个成功；更新进行时的求值只能看到完整的旧版或新版。选做：多个实例共享带版本号的配置。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-feature-flag/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-feature-flag -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把十三条规则和 `acct-1 → 468` 这类数字例子交给它，
一次只给它一个失败的测试，先做校验，再做规则，最后做分桶。分桶的输入、更新的原子方式、返回值是否拷贝这三个设计决定自己留着，
写在给它的指令里。每次改动之后先跑全部测试，再读 diff：它有没有改测试、有没有用 `random` 或 `hash()`、有没有把放量比例塞进哈希、
有没有在原地改已存的配置。最后自己写分桶边界和并发更新的测试，不要让它代写。

**评分点**
- 开工前把合同定成规则：停用先于规则、首个命中赢、属性缺失只算不命中、相等看类型、区间左闭右开、校验先于存储（[[lcp-feature-flag-contract-rules]]）。
- 说得出要存哪些状态：一个字典加一把锁，存冻结的 `Flag`；更新是整份引用替换（[[lcp-feature-flag-state-and-atomic-update]]）。
- 锁内只取引用、锁外计算，返回值与入参都做拷贝，调用方的修改碰不到存储（[[lcp-feature-flag-state-and-atomic-update]]）。
- 分桶只用 `(flag_key, user_id)`，放量比例只移动区间边界，20% 调到 30% 时已入组的用户一个不少（[[lcp-feature-flag-reflection-stable-assignment]]）。
- 不用 `random` 与内置 `hash()`，变体顺序属于分组的一部分（[[lcp-feature-flag-reflection-stable-assignment]]）。
- 多实例时只共享带版本号的配置，各实例本地缓存快照，版本只前进（[[lcp-feature-flag-reflection-multi-instance]]）。
- 能在智能体写出的实现里找出常见缺陷（把布尔当数字、比例进哈希、原地改存储）并给出能抓住它们的测试（[[lcp-feature-flag-contract-rules]]）。

**题解**：[[solution-lcp-feature-flag]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

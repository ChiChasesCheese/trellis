---
nodes: [lcproject.lcp-transactions-list, data.defensive-copy, oop.values, structure.state-machines]
tags: [problem]
---
# Drill：交易列表视图模型（Transactions List）

账单页要显示一份交易列表：每行有地址、城市、金额和日期，页头可以切换全部、收入、支出。后台会推来新的列表，页面要换内容但不能丢掉用户选的筛选。
你补全一个视图模型类，界面和 HTTP 层已经有了；列表至多 1000 条，调用顺序执行，不考虑并发。计划用时 45 分钟，最后留出时间写两篇关于筛选保留与隔离检查的短文。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 10 分钟）：先把 `starter.py` 文档字符串里的六条规则逐条改写成断言。然后做构造、`snapshot` 与筛选：
  三个筛选项顺序固定、恰好一个为真；一条可见交易一个展示项、保持输入顺序；展示项的 `id` 是交易的 `id`；没有匹配时筛选仍然生效。
- 第 2 关（约 10 分钟）：`replaceTransactions`。整体替换、不合并不排序，当前筛选保持并立刻作用在新列表上；初始与替换都可以为空。
  先选支出、再换成只含收入的列表，断言筛选仍是支出且 `items` 为空。
- 第 3 关（约 15 分钟）：隔离。调用方在构造或替换之后改嵌套地点、改金额、清空列表，视图不变；快照被随便修改后再取一次，视图不变；
  旧快照在之后的选择与替换后保持原样；两个实例互不影响。先让这些测试在「保存引用」和「只做浅拷贝」的版本上失败，再修。
- 第 4 关（选做，约 10 分钟）：口述三件合同之外的事：未知筛选名怎么拒绝、十万行时快照怎么变、两个线程同时选择与替换时哪两个字段要合成一个。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-transactions-list/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-transactions-list -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把六条规则和一个小例子（三条交易，选支出，换成空列表）交给它，
一次只给它一个失败的测试，先做筛选，再做换列表，最后做隔离。数据怎么存（冻结的行还是保存引用）、筛选放在哪里、快照是否每次新建，
这三个决定自己留着，写在给它的指令里。每次改动之后先跑全部测试，再读它写的 `__init__`：有没有保存传入的列表、有没有只做浅拷贝、有没有返回内部列表、
有没有在换列表时顺手重置筛选。最后自己写隔离测试，不要让它代写。

**评分点**
- 开工前把合同定成规则：三个筛选恰好一个生效、没有匹配也不退回、展示项取交易的 `id`、换列表保留筛选、字符串原样（[[lcp-transactions-list-contract-rules]]）。
- 说得出要存哪些状态：一个筛选名加一个冻结行的元组，进口读一次、出口每次新建（[[lcp-transactions-list-state-and-invariant]]）。
- 能讲清保存引用与浅拷贝各漏掉什么：清空列表会让视图变空，改嵌套地址会穿透进来（[[lcp-transactions-list-state-and-invariant]]）。
- 筛选与列表是两个独立字段，选择只写前者、替换只写后者，所以保留不靠记性（[[lcp-transactions-list-reflection-keep-filter]]）。
- 给出能抓住缺陷的测试：选支出再换成只含收入的列表、从未选过筛选就换列表、重复选择（[[lcp-transactions-list-reflection-keep-filter]]）。
- 隔离检查分四个方向：输入、快照、历史快照、实例，每个方向先拍下整份期望再破坏再比较（[[lcp-transactions-list-reflection-ownership-and-history]]）。
- 能在智能体写出的实现里找出常见缺陷并给出会失败的测试（[[lcp-transactions-list-reflection-ownership-and-history]]）。

**题解**：[[solution-lcp-transactions-list]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

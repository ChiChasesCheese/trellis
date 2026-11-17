---
nodes: [lcproject.lcp-payments-api, structure.storage, api.error-contract]
tags: [problem]
---
# Drill：付款记录接口（Payments API）

一个小型账户服务：每个账户有一串付款，余额就是付款金额之和；数据在 SQLite 文件里，重启之后账户、付款和编号都得还在。
HTTP 层已经写好，你补三个函数：建账户、查账户与余额、给账户记付款。计划用时 45 分钟，最后留出时间写两篇短文：怎样区分空账户与缺失账户，怎样验证余额与持久化。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的九条规则逐条改写成断言。
  然后做核心流程：`create_account` 得 `Account(1, 0)`；`create_payment(db, 1, 700)` 得 `Payment(1, 1, 700)`；再记 1300 得 `Payment(2, 1, 1300)`；`get_account(db, 1)` 得 `Account(1, 2000)`。
- 第 2 关（约 10 分钟）：缺失与零。`get_account(db, 77)` 与 `create_payment(db, 77, 5)` 都得 `None`；空账户的余额是 0，不是 `None`；
  写一个测试：缺失账户的付款失败三次之后，真账户的第一笔付款 id 仍是 1。
- 第 3 关（约 10 分钟）：持久化。记两笔付款，关库重开，下一笔付款 id 是 3；两个库文件各自从 1 开始；函数没有关你的连接。
- 第 4 关（选做，约 10 分钟）：数值与 HTTP。五笔 +10 亿再两笔 −10 亿，余额 30 亿且是 `int`；起已经写好的适配器，用 `curl` 走一遍 201、200、404；
  再写一个对拍测试：固定种子的随机操作同时喂数据库和一个字典模型，中间随机关库重开。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-payments-api/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-payments-api -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把九条规则和第 1 关的数字例子交给它，一次只给它一个失败的测试，先做建账户与记付款，再做查余额，最后做缺失与重开。
"余额现算、存在性问账户表、缺失账户的付款用条件插入"这三个设计决定自己留着，写在给它的指令里。每次改动之后先跑全部测试，再读 diff：
它有没有给账户表加余额列、有没有先查后写、有没有用 `TOTAL`、有没有在函数里关连接或提交、有没有改测试。最后自己写那两个最要紧的测试（缺失账户的付款不耗 id、空账户余额是 0），不要让它代写。

**评分点**
- 开工前把合同定成规则：缺失是 `None`、余额是求和、失败不耗 id、两条序列独立、重开不丢、连接归调用方（[[lcp-payments-api-contract-rules]]）。
- 说得出状态与不变量：只存两张表，余额现算，存在性问账户表，id 只增不复用（[[lcp-payments-api-state-and-invariant]]）。
- 说清空账户与缺失账户怎么分开：从账户表出发加子查询，`COALESCE` 成 0，内连接与只求和各错在哪（[[lcp-payments-api-reflection-existing-vs-missing]]）。
- 说清怎样不依赖查询写法地验证：数字例子、字典模型对拍、夹着重开、只经公开函数观察（[[lcp-payments-api-reflection-verify-balances]]）。

**题解**：[[solution-lcp-payments-api]]——先做，再看。同样"余额由流水推出"的内存版见 [[solution-bank-account]]、[[solution-digital-wallet]]。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

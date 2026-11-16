---
nodes: [lcproject.lcp-scheduled-banking, structure.state-machines, errors.boundary-validation]
tags: [problem]
---
# Drill：带定时付款的银行账本（Scheduled Banking Ledger）

一个内存银行账本，只有 `Bank` 一个类、九个方法：开户、存款、转账、整批转账、安排与取消定时付款、合并账户、支出排名、任意过去时刻的余额。
调用按严格递增的时间戳顺序到来，没有时钟，付款在到期之后的第一次调用里才真正执行。计划用时 60 分钟，最后留出时间写三篇关于崩溃、历史和并发的短文。

**分关要求**（每关做完再看下一关，像真实的项目轮）
- 第 1 关（约 15 分钟）：先读合同，把 `starter.py` 文档字符串里的十三条规则逐条改写成自己的断言。
  只做开户、存款、转账、排名：失败返回 `None` / `False`，不抛异常；`a` 存 100、转 `b` 40 得到 `60`，`top_spenders(…, 1)` 得 `["a(40)"]`；
  排名先按累计转出降序、再按 ID 的 Python 字符串顺序升序，`"B"` 排在 `"a"` 之前。
- 第 2 关（约 15 分钟）：定时付款。`a` 有 100，第 3 个时刻安排 30、延迟 2，第 5 个时刻存 10 得到 `80`；每个公开方法（含查询与失败的调用）先结算；
  十笔同刻到期的付款里 `payment10` 排在 `payment9` 之后；余额不够就永久失败，同刻的存款救不了；到期那一刻取消已经太晚。
- 第 3 关（约 15 分钟）：合并与历史。`b` 并入 `a` 之后，`get_balance(6, "a", 4)` 仍是 `a` 自己原来的余额，`get_balance(7, "a", 5)` 是合并后的总额，
  被并掉的 `b` 查任何时刻都是 `None`，它的 ID 也不能再开户；付款随合并换主人，编号与顺序不变；付款的余额变化记在到期时刻。
- 第 4 关（约 10 分钟）：整批转账全有或全无。`[("a","b",70),("b","a",20)]` 得 `[30, 50]`；第二批失败得 `None` 且什么都没留下；
  批前已结算的付款保留；空批次返回 `[]` 且仍然结算；净额为零也计入支出；不修改传入的列表。选做：把每个公开方法放进同一把锁，写三篇短文。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-scheduled-banking/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --no-project --python 3.11 --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-scheduled-banking -q`。

**和编程智能体一起练**：用 Claude Code 或工作区里的智能体打开 `starter.py`，把十三条规则和三个数字例子交给它，一次只给它一个失败的测试，
先让它做第 1 关，再做定时付款。"每个入口先结算""付款记在到期时刻""批次先演算后提交""被并掉的 ID 不可复用"这几个设计决定自己留着，写在给它的指令里。
每次改动之后先跑全部测试，再读 diff：它有没有改测试、有没有改公开签名、失败的调用有没有漏掉结算、批次失败时有没有碰真实状态。
最后自己写那几个最要紧的测试（十笔同刻到期、到期时刻的失败转账、恰好花光、净额为零的批次），不要让它代写。

**评分点**
- 开工前把合同定成规则：每次调用先结算、失败用返回值、批次整体提交、历史记在事件时刻（[[lcp-scheduled-banking-contract-rules]]）。
- 付款按（到期时间, 序号的数值）排队，钱不够永久失败，同刻存款救不了，到期那一刻取消已太晚（[[lcp-scheduled-banking-contract-rules]]）。
- 说得出要存的状态：每账户一条余额时间线、到期堆加按编号的字典、用过的 ID 集合，以及"时间线只前进、先校验后写入"的不变量（[[lcp-scheduled-banking-state-and-invariant]]）。
- 历史用二分查"最近的不晚于 `time_at` 的点"，合并只追加一个点而不追溯，取消留下的残留项有界（[[lcp-scheduled-banking-state-and-invariant]]）。
- 能说清崩溃后付款如何安全重试：状态落库、扣款与改状态同一事务、付款编号做幂等键（[[lcp-scheduled-banking-reflection-crash-safe-payments]]）。
- 能说清并发下必须原子的是"结算 + 校验 + 写入"整个公开方法，只锁字典为什么不够，分片后如何避免死锁（[[lcp-scheduled-banking-reflection-concurrent-atomicity]]）。
- 给编程智能体的第一条指令带着合同和数字例子，拆小步，自己留着结算范围与批次原子性这些决定（[[lcp-scheduled-banking-contract-rules]]）。

**题解**：[[solution-lcp-scheduled-banking]]——先做，再看。经典版本见 [[solution-bank-account]]。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

---
nodes: [lcproject.lcp-loan-management, fsm.illegal-transitions, concurrency-depth.compound-actions, data.defensive-copy, ai.verification]
tags: [problem]
---
# Drill：贷款生命周期修复（Loan Lifecycle）

一个内存里的贷款服务：借款人创建贷款，出借人放款，借款人分次还款。线上现象是创建完的贷款查不到、放款后余额对不上、同一笔贷款被放款两次、还款无缘无故失败。
规模是一个服务类，几十行；难点是缺陷互相遮盖（顺序、比较方向、状态检查、别名），而且"只放款一次"只在并发下才露馅。

**分关要求**（每关做完再看下一关，像真实的修复轮）
- 第 1 关（约 15 分钟）：先不改代码，把十条规则逐条对照现有服务，写出差异清单（编号、存放位置、快照、状态检查、比较方向、扣款顺序、还清状态、构造时复制），再跑一遍测试看哪些失败。每处缺陷先写一个会失败的最小测试。
- 第 2 关（约 20 分钟）：修创建与查询：编号只给成功的创建，贷款用返回的编号作键存入，`get` 返回快照，构造时复制余额；再修放款：贷款存在 → 出借人存在 → 状态与身份 → 余额，余额恰好等于本金也行，转账成功后状态才变。
- 第 3 关（约 20 分钟）：修还款：金额 → 贷款 → 归属 403 → 状态与超额 409 → 余额；先检查完再划转，失败时贷款与余额纹丝不动；还清变 repaid，部分还款仍是 active。用"同时违反两条规则"的输入测检查顺序。
- 第 4 关（选做，约 15 分钟）：并发：十六个线程同时给同一笔贷款放款，恰好一个成功；一个出借人同时给十笔贷款放款，成功的笔数不超过余额能付的；二十个线程各还 10，总额不超过欠款。然后写三个书面回答：只放款一次的不变量与测法；搬到共用数据库时锁换成什么；还款幂等与禁止超额的区别。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-loan-management/starter.py` 里的 `LoanService` 当作要修的服务，改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-loan-management -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给十条规则和一个数字例子（借 60、放款、还 20，余额 40 和 60），要求它只列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一类缺陷、只给它一个失败的测试，改完立刻运行测试。
检查顺序、锁罩住哪些对象、状态转移的前提放在哪里，这些设计决定自己留着；期望值自己独立写出，不接受"把测试改成通过"，也不让它为了过测试把比较方向改来改去。

**评分点**
- 写得出开工前的合同：金额只认正 int、放款与还款的检查顺序、状态单向、失败不留痕、余额守恒、返回快照（[[lcp-loan-management-contract-rules]]）。
- 说得清服务要存哪些状态，为什么"检查 pending"与"扣款并改 active"必须在同一次持锁里，以及怎样用屏障测"恰好放款一次"（[[lcp-loan-management-state-and-invariant]]）。
- 知道搬到共用数据库时，锁换成事务加条件更新：状态抢占、带下限扣款、固定顺序加锁（[[lcp-loan-management-reflection-shared-database]]）。
- 分得清还款的超额检查与幂等：一个看贷款状态，一个看请求身份，以及同号同内容重放、同号不同内容冲突（[[lcp-loan-management-reflection-repay-idempotency]]）。
- 写得出能抓住缺陷的测试：已放款的贷款被穷出借人再放款、创建后立即查询、返回值被改后服务不变、屏障下的并发放款（[[lcp-loan-management-contract-rules]]、[[lcp-loan-management-state-and-invariant]]）。

**题解**：[[solution-lcp-loan-management]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

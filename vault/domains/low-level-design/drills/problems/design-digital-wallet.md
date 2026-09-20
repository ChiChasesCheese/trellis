---
nodes: [problems.marketplaces.digital-wallet, concurrency.hazards]
tags: [problem]
---
# Drill：数字钱包（Digital Wallet）

一个进程内的钱包服务：用户开户、充值、提现、互相转账，随时能查余额和交易记录。金额一律
是**整数最小货币单位（分）**，余额永远不能为负，转账的两边必须精确一致。几十个账户、
每个账户几千笔历史交易、转账双方经常同时被别的转账触碰。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：开户、充值、提现、转账、查余额。动手前先决定钱用什么类型
  （别用 `float`，想清楚为什么）。不合法的操作（金额非正、账户不存在、转账双方是同一个
  账户、转出方余额不够）当场拒绝，而且**两边余额都不能被改动**。
- 第 2 关（约 15 分钟）：把每一次资金移动记成账本里的**两条分录**，相加为零。余额是每次
  从账本现算，还是缓存并定期核对？两种都要能说出代价，选一种写下来。写一个随机会话测试：
  固定种子、几百次随机的充值/提现/转账，**全部做完之后**断言账本全局相加为零，且每个
  账户的余额和账本重新推导出的值完全一致。
- 第 3 关（约 15 分钟）：转账要同时锁住转出和转入两个账户。**这一关的分数全在加锁顺序
  上**：按账户 id 这样的稳定键排序，还是按参数 `(from, to)` 的顺序？把两个方向的并发
  转账会不会互相等出死锁讲清楚，再用真实线程验证——两组线程同时按相反方向高频转账，
  断言在有限时间内跑完、金额守恒。
- 第 4 关（选做）：带分页的交易记录，或者幂等转账（同一个 `client_key` 重试绝不能把钱
  移动两次，且要能分辨"这是重试"和"这是另一笔参数不同的转账"）。评分点不是"写出来了"，
  而是**加它有没有动到第 2 关账本的任何一行**。

**怎么练**：把 `vault/domains/low-level-design/problems/digital-wallet/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/digital-wallet -q`。

**评分点**
- 钱用整数最小货币单位，不用 `float`；说得出为什么"份额之和/两条分录之和"这类等式在
  浮点数下会悄悄崩掉（[[problems-digital-wallet-transfer-atomicity]]）。
- 每一次资金移动（包括充值和提现，不只是转账）都落成账本里两条相加为零的分录；说得出
  充值/提现怎么被纳入同一套双分录表示而不是单独开一条特殊路径
  （[[problems-digital-wallet-external-account]]）。
- 分录用带符号的 `delta` 表达方向，而不是 `kind` 加金额两个互相要保持一致的字段；说得出
  为什么这里 Enum 是多余的（[[problems-digital-wallet-signed-delta-not-kind]]）。
- 余额缓存还是现算，选了一种并说得出取舍；缓存方案要能定期核对、纠正漂移
  （[[problems-digital-wallet-balance-cache-vs-derive]]）。
- 转账加锁按账户 id 等稳定键排序，不按参数顺序；说得出按参数顺序会在两个方向的并发转账
  之间造成什么样的环形等待（[[problems-digital-wallet-lock-ordering-stable-key]]、
  [[concurrency-lock-ordering-transfer]]）。
- 转出方余额不足时，两边余额都原封不动；校验发生在真正落账之前，没有"先扣后回滚"的路径
  （[[problems-digital-wallet-transfer-atomicity]]）。
- 幂等靠复用转账本身的两把账户锁，不额外建一张永不清理的锁表；能分辨"同一个 key 的重试"
  和"同一个 key 用在了不同参数上"这两种情况，后者要报错而不是静默放过
  （[[problems-digital-wallet-idempotency-reuses-account-lock]]、
  [[problems-digital-wallet-idempotency-conflict]]）。
- 每个容器都有出口：幂等缓存能按时间清理；账本本身的分录表相反，故意不清——说得出为什么
  这两者的答案不一样（[[problems-digital-wallet-ledger-append-only-idempotency-purged]]）。

**题解**：[[solution-digital-wallet]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

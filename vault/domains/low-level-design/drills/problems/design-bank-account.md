---
nodes: [problems.marketplaces.bank-account, structure.storage]
tags: [problem]
---
# Drill：银行账户系统（Bank Account System）

一份分关递进的机考题（CodeSignal 一类工业级编码评测的格式）：一次性给出四关的文档，
每写完一关提交一次，评测系统跑一批看不见代码的隐藏测试。所有"过了多久"都由方法参数里
显式传入的时间戳决定，没有真实的墙上时钟或后台线程。

**分关要求**（每关做完再看下一关，像真实的机考一样——先把这一关的本地测试跑绿再往下看）
- 第 1 关（约 20 分钟）：开户、存款、转账、查余额。动手前先想清楚："后面几关大概率会
  要什么"（排行？时间？合并？）——选一个经得住这三次考验的核心表示，不要只为第 1 关
  最省事的写法。
- 第 2 关（约 15 分钟）：按截至某个时间戳的转账支出总额，取前 N 个账户排行。支出相同
  时打平规则是什么？说得出为什么"确定的排序结果"比"哪种规则听起来更合理"更重要。
- 第 3 关（约 20 分钟）：定时支付——立即扣款，一段延迟之后返现；支持在返现落地之前取消。
  没有后台线程，"到期"只在下一次任意调用发生时才被处理。想清楚：返现记进账本时用哪个
  时间戳？触发结算的那次调用，还是真正到期的那一刻？
- 第 4 关（约 15 分钟）：合并两个账户——余额、历史、还没返现的定时支付都要正确过渡到
  存活账户，且被合并掉的账户 id 依然要能回答合并之前任意时刻的历史余额查询。

**怎么练**：把 `vault/domains/low-level-design/problems/bank-account/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/bank-account -q`。

**评分点**
- 核心表示是一份只增不减的事件日志，不是账户身上一个可变的余额字段；说得出后面三关
  分别会让"可变字段"这条路走不通在哪里（[[problems-bank-account-event-log-vs-mutable-balance]]）。
- 写操作（开户/存款/转账/定时支付/合并）拒绝比上一次调用更早的时间戳，只读的余额查询
  却必须接受任意历史时刻；说得出为什么这两条规则不能是同一条
  （[[problems-bank-account-read-write-timestamp-split]]）。
- 定时支付完全没有用到 `time.sleep` 或任何后台定时器，"过了多久"是调用方传入的一个
  普通参数（[[problems-bank-account-timestamp-argument-not-real-clock]]）。
- 懒惰结算的返现记在**真正到期的那一刻**，不是触发结算的那次调用的时间；能说出一个
  反例证明用错时间戳会导致历史查询漏算
  （[[problems-bank-account-cashback-recorded-at-maturity-not-trigger]]）。
- 排行支出相同时按账户 id 升序打平，结果确定、可复现
  （[[problems-bank-account-top-spenders-tie-break]]）。
- 合并账户不搬迁、不复制任何一条历史记录，只是把 id 标记为不再活跃；被合并账户的历史
  余额查询用的是和合并之前完全相同的归约逻辑
  （[[problems-bank-account-merge-freezes-not-deletes]]）。
- 合并时把被合并账户名下还未结算的定时支付改指到存活账户，返现到账时才不会落进一个
  没人再查的死账户（[[problems-bank-account-payment-follows-account-on-merge]]）。
- 账户 id 一旦用过就永久保留，即使对应账户已经被合并掉，也不能把这个 id 分配给一个
  全新的账户（[[problems-bank-account-id-never-reused]]）。

**题解**：[[solution-bank-account]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

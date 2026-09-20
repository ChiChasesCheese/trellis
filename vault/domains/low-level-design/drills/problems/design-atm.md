---
nodes: [problems.machines.atm, patterns.state, structure.state-machines, concurrency.primitives]
tags: [problem]
---
# Drill：ATM 取款机（ATM）

一台街边的 ATM：插卡、输密码、取款存款查余额、退卡。钞票在机器的钞箱里，余额在银行的账户上，
中间隔着一条会超时的网络——**这道题的全部难度都压在"两个权威之间没有事务"这一句上**。
金额一律用整数分，面额是 10／20／50／100 元。照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：会话状态机 IDLE → 已插卡 → 已认证 → 出钞中 → 已认证 → IDLE，并且
  **每一个非法顺序都被按名字拒绝**：没插卡就取款、没输密码就查余额、出钞过程中退卡。一次
  认证可以连做多笔交易。密码连错三次：卡被机器留下，账户被银行冻结——先想清楚这两个效果
  分别归谁。另外，插卡那一刻不许验证任何东西，想想为什么。
- 第 2 关（约 20 分钟）：取款。钞票必须从**钞箱里实际装着的面额**中凑出来，所以"凑不出"是
  一个一等公民的业务结果，不是 `assert`；而且它不止一种理由，至少分得出三种。然后定下
  取款的操作顺序（扣账和吐钞谁先），并说得出另外两种顺序各自在什么时候丢钱。任何失败路径
  上，钞箱和余额都必须**逐项不变**。
- 第 3 关（约 15 分钟）：存款、查余额，以及一条只增不改的流水。再加一条真实路径：客户没把
  钱取走，机器超时收回——钞票该进哪个箱？账怎么平？原来那条流水要不要改？最后写一个对账
  方法，把"这台机器没吞钱"变成一行可断言的等式。
- 第 4 关（选做）：接受另一家银行的卡。跨行转接网络（按卡号前缀路由、收一笔手续费）已经
  写在测试文件里了，你**不需要**实现它——这一关要验的恰恰是反面：把它传进你的 ATM，机器
  能不能一行不改就跑通。所以判分点只有一个：状态枚举、转移表、钞箱、选钞、流水全都不许动。
  如果你发现自己要往状态里加成员，回头看第 1 关把什么混进了会话状态。顺带想一条策略：
  这笔取款被冲正时，跨行手续费该不该一起退？

**怎么练**：把 `vault/domains/low-level-design/problems/atm/starter.py` 的方法体补全，然后在
仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/atm -q`。

**评分点**
- 说得出账户和 ATM 各自拥有哪条不变式，并且网络协议里**没有** `get_account()`（[[problems-atm-two-authorities]]）。
- 取款的操作顺序定成"先留钞 → 再扣账 → 最后交钞"，并说得出另外两种顺序各丢什么（[[problems-atm-order-of-operations]]）。
- 扣账成功但钱没到手时发冲正而不是自己改余额，原流水保持不变、新增一条（[[problems-atm-reversal-not-rollback]]）。
- 把"取不出"分成金额不可表示／库存凑不出／张数超限三种，并说得出第一种和库存无关（[[problems-atm-three-dispense-failures]]）。
- 选钞是一个可替换的纯函数而不是责任链，默认实现保证有解必找得到（[[problems-atm-note-selection-no-chain]]）。
- 密码错误计数归发卡行、吞卡归机器，并能写出"三台机器各错一次"的测试（[[problems-atm-pin-counter-owner]]）。
- 卡不存在和密码错误报同一个错，插卡时不验证任何东西（[[problems-atm-enumeration-oracle]]）。
- 拒绝 `Transaction` 继承体系，用三个方法加一条不可变流水；说得出什么时候才该用 Command（[[problems-atm-refuse-transaction-hierarchy]]）。
- 写得出钞票守恒等式并让它随时可验（[[problems-atm-cash-conservation-invariant]]）。
- 第二家银行靠一个真有两个实现的协议接入，路由键藏在账户标识里（[[problems-atm-second-bank-adapter]]）。
- 说得清超时和失败的区别，以及 `ref` 幂等重试（[[problems-atm-network-timeout-idempotency]]）。
- 锁加在账户上、说得出 GIL 为什么不够，并发测试用屏障断言不变式（[[problems-atm-account-lock-and-gil]]、[[concurrency-check-then-act]]）。

**题解**：[[solution-atm]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

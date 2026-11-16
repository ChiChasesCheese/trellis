---
nodes: [lcproject.lcp-password-reset, fluency.time-numbers, fsm.illegal-transitions, data.defensive-copy, testing.doubles]
tags: [problem]
---
# Drill：密码重置修复（Password Reset）

一个密码重置服务让用户请求一个重置码，30 秒内凭码改密码。现有代码能跑，但配置地址被改写、码会重复、有效期比较了钟面字段、旧的无时区时间按本地时区猜、密码改在副本上没保存、成功后不清记录。规模是一个文件、几十行；难点是几处缺陷互相叠加，只看最后的返回值分不清是哪处错了。

**分关要求**（每关做完再看下一关，像真实的修复轮）
- 第 1 关（约 10 分钟）：先不改代码，把十五条规则逐条对照现有代码，写出差异清单；再修配置与请求：地址在构造时快照、原样保留空串与空白、空映射也算"给了"、构造与未知用户都不读时钟、码不重复。每处先写一个会失败的测试。
- 第 2 关（约 10 分钟）：修校验与有效期：`[0, 30)` 秒，两端都换成 UTC，旧的无时区时间当 UTC。每个边界写两个测试：恰好边界和前后一格；把进程时区改成非 UTC 再测旧记录。
- 第 3 关（约 10 分钟）：修保存与消耗：成功时一次 `update_password`、再清记录；重放（含换实例）得 `False`；再请求可再改；用户之间互不影响，被删用户的残留记录返回 `False`。用一个记录写入顺序的存储替身断言。
- 第 4 关（选做，约 15 分钟）：写三个书面回答：并发下怎样让改密码与消耗原子；上线前改码的生成、存储与密码哈希的哪几处；多实例共享数据库时怎样限制尝试次数并让过期可靠。

**怎么练**：把 `vault/domains/low-level-design/problems/lcp-password-reset/starter.py` 当作要修的服务，改完后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/lcp-password-reset -q`。

**和编程智能体一起练**：用编程智能体（Claude Code 或工作区自带的智能体）打开 `starter.py`。第一条指令给规则和两个数字例子（29.9 秒有效、30 秒过期），要求它先列出代码与规则的差异、不改代码；你核对清单后，一次只让它修一类缺陷、只给它一个失败的测试，改完立刻运行测试。时间边界、旧记录怎么解释、成功路径的写入顺序这些决定自己留着；期望值自己独立写出，不接受"把测试改成通过"。

**评分点**
- 写得出开工前的合同：配置快照、码唯一、半开的 30 秒、失败不留痕、先存后消耗、用户隔离（[[lcp-password-reset-contract-rules]]）。
- 说得清服务要记什么、库里要存什么，以及"一个码最多成功一次"这条不变量（[[lcp-password-reset-state-and-invariant]]）。
- 知道多进程下用库里带条件的删除，而不是进程内的锁；次数与过期也放在库里（[[lcp-password-reset-reflection-shared-database]]）。
- 知道上线前要改的三处：安全随机数、只存摘要加常量时间比较、加盐慢哈希（[[lcp-password-reset-reflection-credential-hardening]]）。
- 写得出能抓住缺陷的测试：边界两侧、非 UTC 机器上的旧记录、同一个时区对象跨偏移、整个存储的快照比较（[[lcp-password-reset-contract-rules]]、[[lcp-password-reset-state-and-invariant]]）。

**题解**：[[solution-lcp-password-reset]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：

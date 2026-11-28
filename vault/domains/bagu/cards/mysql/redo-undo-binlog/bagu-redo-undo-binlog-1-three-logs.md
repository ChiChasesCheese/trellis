---
id: bagu-redo-undo-binlog-1-three-logs
node: a.mysql.redo-undo-binlog
type: qa
step: 1
---
## Q
**三种日志 · redo log、undo log、binlog 各是什么，为什么缺一不可**｜必会

面试官：「redo log、undo log、binlog 各是什么、解决什么？binlog 不是已经记录所有修改了吗，为什么还要 redo log？」

## A
**基本回答。** 三种日志各管一件事。redo log（重做日志）在 InnoDB 层，记录「对某个数据页做了什么修改」，崩溃后把已提交但还没刷到磁盘的修改重做一遍，保证持久性，写满后循环覆盖，大小固定。undo log（回滚日志）也在 InnoDB 层，记录修改前的旧值，用于回滚和 MVCC（多版本并发控制）。binlog（二进制日志）在 Server 层，所有存储引擎共用，记录逻辑变更（ROW 格式记每行改成了什么），只追加不覆盖，用于主从复制和按时间点恢复。
为什么要日志：改动先发生在内存页（InnoDB 一页 16KB），没写盘就断电已提交事务会丢，做到一半失败又要撤回，所以一种日志记「改了什么」重做，一种记「原来是什么」撤销。8.0.30 起 redo 由 `innodb_redo_log_capacity` 控制（默认 100MB，在线可调，放 `#innodb_redo` 目录），之前是固定的 `ib_logfile0/1`。binlog 默认保留 30 天（`binlog_expire_logs_seconds` = 2592000）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Server 层：所有存储引擎共用</text>
<rect x="8" y="20" width="324" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">binlog（逻辑日志，追加写）</text>
<text x="170" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">记「每行改成什么」→ 复制、时间点恢复</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">InnoDB 层：只有 InnoDB 有</text>
<rect x="8" y="90" width="158" height="60" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">redo log</text>
<text x="87" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">记数据页改了什么</text>
<text x="87" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">循环写 · 崩溃重做</text>
<rect x="174" y="90" width="158" height="60" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="253" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">undo log</text>
<text x="253" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">记修改前的旧值</text>
<text x="253" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回滚 · MVCC</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">redo：提交了不能丢</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">undo：没提交要能撤</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">binlog：别的库追上，出错回到某时刻</text>
</svg>
先分层：binlog 在上层（Server），谁用存储引擎都有；redo 和 undo 在下层（InnoDB），是引擎自己的事。下面三行是口诀，一行对应一个日志。
**举个例子。** 一笔转账把账户 1 的余额从 100 改成 50，三份日志各记了什么：
1. **undo log：**「账户 1 的余额旧值是 100」。事务回滚时照着写回 100。
2. **redo log：**「第 X 个数据页的这个位置改成 50」。事务提交后断电，重启时照着把页改成 50。
3. **binlog：**「表 account 里主键为 1 的行，余额由 100 变成 50」（ROW 格式）。从库收到后执行同样的修改。
4. **去掉 redo 会怎样：** 提交成功后断电，内存里改成 50 的页没来得及写盘，重启后余额还是 100，已提交的转账丢了。
5. **去掉 undo 会怎样：** 事务做到一半失败，已经改了内存的页没法撤回，余额停在中间状态。
6. **去掉 binlog 会怎样：** 主库自己没事，但从库永远收不到这笔变更，备份也无法恢复到误操作之前。
**容易错。**
- **以为 binlog 能代替 redo：** binlog 是逻辑日志，不记页的状态，崩溃后不知道从哪里重放，保证不了 InnoDB 的持久性。
- **以为 redo 能代替 binlog：** redo 循环覆盖，历史会被覆盖掉，做不了时间点恢复，也没法给从库用。
- **以为三种日志都在引擎层：** 只有 redo 和 undo 是 InnoDB 的；binlog 在 Server 层，所有引擎共用。
- **以为 undo 只管回滚：** 它同时是 MVCC 的历史版本来源，所以提交后也不能马上删。

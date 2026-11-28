---
id: bagu-redo-undo-binlog-4-two-phase
node: a.mysql.redo-undo-binlog
type: qa
step: 3
---
## Q
**两阶段提交 · 为什么存在，不同阶段崩溃怎么恢复**｜必会

面试官：「两阶段提交是什么流程？为什么需要？不同步骤崩溃，重启后怎么处理？」

## A
**基本回答。** 一次提交要让 redo 和 binlog 同时生效，两阶段提交（two-phase commit）保证两份日志对同一个事务的结论一致。流程：先执行更新，改缓冲池里的页，写 undo 和 redo；第一阶段，把 redo 写成 prepare 状态并刷盘；然后写 binlog 并刷盘；第二阶段，把 redo 写成 commit。崩溃恢复时扫描 redo，遇到 prepare 状态的事务，就按事务 ID（XID）去 binlog 里找：binlog 里有完整记录就提交，没有就回滚。
redo 和 binlog 是两个文件，不可能同时写完，写了一份就崩溃会让主库、从库、备份看法不一致。两份日志都不丢要 `innodb_flush_log_at_trx_commit=1` 加 `sync_binlog=1`。binlog 提交又分 flush、sync、commit 三阶段，每阶段由一个 leader 带一队事务合并 fsync。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<rect x="8" y="6" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 改页，写 undo、redo</text>
<rect x="8" y="58" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② redo 写 prepare 并刷盘</text>
<rect x="8" y="110" width="170" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="93" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 写 binlog 并刷盘</text>
<rect x="8" y="162" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ redo 写 commit</text>
<line x1="93" y1="34" x2="93" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,58.0 89.8,51.0 96.2,51.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="93" y1="86" x2="93" y2="104" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,110.0 89.8,103.0 96.2,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="93" y1="138" x2="93" y2="156" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,162.0 89.8,155.0 96.2,155.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="190" y="46" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">崩：还没 prepare → 回滚</text>
<text x="190" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">崩：binlog 没有 → 回滚</text>
<text x="190" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩：binlog 完整 → 提交</text>
<text x="190" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">commit 后崩 → 无事</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">prepare 的事务：按 XID 去 binlog 找，完整就提交</text>
</svg>
左边是四步，右边写在每两步之间崩溃时的处理结果。关键只有一条：处在 prepare 的事务，由「binlog 是否完整」决定生死。
**举个例子。** 转账事务 XID=77：
1. **执行更新：** 余额改成 50，写好 undo、redo。
2. **redo prepare：** 刷盘。此刻断电，重启后看到 XID=77 处于 prepare，去查 binlog，没有它，回滚，余额回到 100。
3. **写 binlog：** 刷盘。此刻断电，重启后 XID=77 处于 prepare，binlog 里有完整记录，于是提交，主库余额是 50。从库本来就会收到这条 binlog，也是 50，两边一致。
4. **redo commit：** 写完后断电，没有悬而未决的事务，什么都不用做。
5. **半截 binlog：** 如果 binlog 只写了一半，不完整，等同于没有，回滚；从库也不会执行半条事务。
**容易错。**
- **以为 prepare 之后一定回滚：** 要看 binlog，binlog 完整就提交，不是一律回滚。
- **以为 binlog 完整就不需要 redo commit：** commit 是第二阶段的收尾，恢复时靠 binlog 补提交；正常运行要写完整的 commit 才算结束。
- **以为两阶段提交是分布式事务那套：** 这里是同一个数据库内两份日志之间的两阶段，目的只是让 redo 和 binlog 一致。
- **忘了代价：** 一次提交至少两次 fsync，所以才需要组提交。

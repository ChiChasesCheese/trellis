---
id: bagu-redo-undo-binlog-5-binlog
node: a.mysql.redo-undo-binlog
type: qa
step: 5
---
## Q
**binlog · 有哪几种格式，主从复制怎么用它**｜追问

面试官：「binlog 有哪几种格式？区别是什么？主从复制流程是怎样的？」

## A
**基本回答。** binlog 有三种格式。STATEMENT 记 SQL 语句本身，体积小，但 `NOW()`、`UUID()`、没有 `ORDER BY` 的 `LIMIT` 这类不确定的语句在从库重放，结果可能和主库不同，导致主从不一致。ROW 记每一行修改前后的内容，主从一致，便于恢复和闪回，但体积大，更新 100 万行就要记 100 万行的镜像。MIXED 默认用 STATEMENT，遇到不安全语句就切成 ROW。5.7.7 起默认是 ROW。复制流程：主库把变更写进 binlog，dump 线程把它发给从库；从库的 I/O 线程把收到的内容写入中继日志（relay log）；SQL 线程（或并行的多个线程）重放中继日志。
用途：主从复制，和按时间点恢复（PITR：全量备份加之后的 binlog，重放到误操作前一刻）。`binlog_row_image` 默认 FULL 记整行，MINIMAL 只记变化的列和主键，体积小但闪回信息可能不够。binlog 在 Server 层，不依赖引擎。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<rect x="8" y="8" width="100" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库</text>
<text x="58" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写 binlog</text>
<rect x="120" y="8" width="100" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库</text>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">relay log</text>
<rect x="232" y="8" width="100" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库数据</text>
<text x="282" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重放结果</text>
<line x1="108" y1="33" x2="114" y2="33" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,33.0 113.0,36.2 113.0,29.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="220" y1="33" x2="226" y2="33" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,33.0 225.0,36.2 225.0,29.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dump 线程发出，I/O 线程收下，SQL 线程重放</text>
<text x="8" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一条 UPDATE 三种格式记的内容</text>
<rect x="8" y="114" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="131" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">STATEMENT</text>
<rect x="112" y="114" width="220" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="131" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SQL 语句，体积小</text>
<rect x="8" y="144" width="100" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58" y="161" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ROW</text>
<rect x="112" y="144" width="220" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="222" y="161" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每行改前改后，体积大</text>
<rect x="8" y="174" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="191" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MIXED</text>
<rect x="112" y="174" width="220" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="191" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">默认 SQL，不安全时切 ROW</text>
<text x="8" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5.7.7 起默认 ROW</text>
</svg>
上半是复制的数据流向：主库的 binlog 经 dump 线程送到从库，落在 relay log，再由 SQL 线程重放进从库数据。下半是三种格式，ROW 是默认。
**举个例子。** 运营误执行 `UPDATE coupon SET status = 0` 漏了条件，几十万张券失效：
1. **STATEMENT 格式：** binlog 里只有这条 SQL，不知道每行原来的 status 是什么，想恢复只能靠备份加重放，很难精确闪回。
2. **ROW 格式：** binlog 里每一行都有修改前的 status，可以解析出来，生成反向 SQL，把几十万行改回原值。
3. **PITR 流程：** 先恢复最近一次全量备份，再用 mysqlbinlog 重放 binlog 到误操作之前的位点，跳过那条语句。
4. **复制路径：** 这条误操作同样被 dump 线程发给了从库，从库也被改了，所以靠从库回退行不通，要靠备份加 binlog。
**容易错。**
- **以为 STATEMENT 更好所以默认它：** 5.7.7 起默认已经是 ROW，一致性优先。
- **以为 ROW 一定很大：** 只有大批量更新才大；可以用 `binlog_row_image=MINIMAL` 缩小，代价是信息少。
- **以为从库能当后悔药：** 误操作也会被复制过去，要靠备份加 binlog 做时间点恢复。
- **以为复制是同步的：** 这里的 SQL 线程是异步重放，从库会有延迟。

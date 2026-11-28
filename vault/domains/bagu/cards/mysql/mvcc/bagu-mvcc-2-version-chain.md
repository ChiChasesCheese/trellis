---
id: bagu-mvcc-2-version-chain
node: a.mysql.mvcc
type: qa
step: 2
---
## Q
**版本链 · 隐藏列和 undo log 怎么串起历史版本**｜必会

面试官：「InnoDB 一行里有哪些隐藏列？旧版本存在哪，怎么串起来？」

## A
**基本回答。** InnoDB 的聚簇索引（clustered index，行数据本身就存在主键索引的叶子上）里，每行都带几个隐藏列：`DB_TRX_ID`（6 字节）是最近一次修改这行的事务 ID；`DB_ROLL_PTR`（7 字节）是回滚指针，指向 undo log 里修改前的那个版本；如果表没有主键也没有合适的唯一索引，还会有 6 字节的 `DB_ROW_ID` 做隐藏行号。每次修改，旧版本先写进 undo，行上的 `DB_TRX_ID` 改成当前事务，`DB_ROLL_PTR` 指向刚写的那条 undo 记录；这条 undo 记录又带着上一个版本的指针，就这样从新到旧串成一条版本链。
删除只是打 delete mark，没有事务再需要旧版本时 purge 线程才清理。undo 分两类：insert undo 提交后即可丢弃；update undo 要等所有可能用到它的读视图结束后才能清理。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="56" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">行上（最新）</text>
<rect x="6" y="24" width="100" height="64" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额=50</text>
<text x="56.0" y="60.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TRX_ID=100</text>
<text x="56.0" y="75.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ROLL_PTR →</text>
<line x1="106" y1="56" x2="120" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,56.0 113.0,59.2 113.0,52.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">undo 记录</text>
<rect x="120" y="24" width="100" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额=100</text>
<text x="170.0" y="60.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TRX_ID=90</text>
<text x="170.0" y="75.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ROLL_PTR →</text>
<line x1="220" y1="56" x2="234" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="234.0,56.0 227.0,59.2 227.0,52.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="284" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">undo 记录</text>
<rect x="234" y="24" width="100" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额=80</text>
<text x="284.0" y="60.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TRX_ID=60</text>
<text x="284.0" y="75.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ROLL_PTR 空</text>
<text x="6" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从新到旧串成一条版本链</text>
<text x="6" y="132" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">DB_TRX_ID：最近改这行的事务 ID（6 字节）</text>
<text x="6" y="150" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">DB_ROLL_PTR：指向 undo 里改前的版本（7 字节）</text>
<text x="6" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">DB_ROW_ID：无主键时的隐藏行号（6 字节）</text>
<text x="6" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读最新版本最快；要旧版本才顺指针去 undo 找</text>
<text x="6" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一份 undo 既用来回滚，也用来给 MVCC 读旧版本</text>
</svg>
最左边是行里的最新版本，每个版本的 `ROLL_PTR` 指向下一个更老的版本；读最新的不用走指针，需要旧版本才往右找。
**举个例子。** 账户行的演变，用事务 ID 标出来：
1. 事务 60 插入这行：余额 80，`DB_TRX_ID=60`，没有更早的版本。
2. 事务 90 把余额改成 100：旧版本 `(80, 事务60)` 进 undo，行变成余额 100、`DB_TRX_ID=90`、`DB_ROLL_PTR` 指向那条 undo。
3. 事务 100 把余额改成 50，还没提交：旧版本 `(100, 事务90)` 进 undo，并带着指向 `(80, 事务60)` 的指针；行变成余额 50、`DB_TRX_ID=100`。
4. 事务 105 来读，发现链头的事务 100 还没提交，不能读；顺着回滚指针到 `(100, 事务90)`，事务 90 已提交，读到 100。
5. 如果事务 100 回滚，就是把 undo 里的 `(100, 事务90)` 恢复到行上。
**容易错。**
- **以为旧版本存在行里：** 行里只有最新版本，旧版本在 undo log 里，靠回滚指针找。
- **以为二级索引也有版本链：** 版本链只在聚簇索引里；二级索引判断可见性要回聚簇索引。
- **以为删除立刻释放空间：** 删除只打标记，purge 线程在没有读视图需要后才清理。
- **以为长事务没副作用：** 长事务让 purge 无法清理，版本链越来越长，读旧版本要走更多步。

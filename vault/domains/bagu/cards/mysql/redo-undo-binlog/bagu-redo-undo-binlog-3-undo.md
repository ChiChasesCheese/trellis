---
id: bagu-redo-undo-binlog-3-undo
node: a.mysql.redo-undo-binlog
type: qa
step: 4
---
## Q
**undo log · 回滚和 MVCC 里分别起什么作用**｜追问

面试官：「undo log 里存什么？回滚怎么用？MVCC 又怎么用？」

## A
**基本回答。** undo 记录的是每次修改的「反操作信息」：插入一行，记下主键，回滚时就把这行删掉；更新一行，记下被改列的旧值，回滚时写回去；删除一行，记录本身先只打删除标记、仍留在页里，undo 只记主键和旧的事务信息，回滚时去掉删除标记。回滚时按相反的顺序逐条执行这些反操作。在 MVCC 里，undo 又保存了行的历史版本，快照读沿回滚指针串成的版本链，找到读视图可见的那一版。同一份 undo 同时服务回滚和一致性读。
8.0 起 undo 默认放独立的 undo 表空间（`undo_001`、`undo_002`），可在线截断；undo 本身的修改也会写 redo。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三种修改，undo 各记什么、回滚做什么</text>
<rect x="8" y="22" width="70" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="43" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">操作</text>
<rect x="78" y="22" width="120" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="138" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">undo 记的</text>
<rect x="198" y="22" width="134" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="265" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回滚时</text>
<rect x="8" y="48" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">插入</text>
<rect x="78" y="48" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="138" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新行的主键</text>
<rect x="198" y="48" width="134" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">删掉这一行</text>
<rect x="8" y="74" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">更新</text>
<rect x="78" y="74" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="138" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">被改列的旧值</text>
<rect x="198" y="74" width="134" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="91" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">把旧值写回</text>
<rect x="8" y="100" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">删除</text>
<rect x="78" y="100" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="138" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主键与事务号</text>
<rect x="198" y="100" width="134" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">去掉删除标记</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">MVCC：同一行的旧版本沿回滚指针串成链</text>
<rect x="8" y="146" width="130" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="73" y="159.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">当前行</text>
<text x="73" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额 50</text>
<rect x="202" y="146" width="130" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="267" y="159.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">undo 旧版本</text>
<text x="267" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额 100</text>
<line x1="138" y1="163" x2="196" y2="163" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="202.0,163.0 195.0,166.2 195.0,159.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">指针</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">快照读沿链找读视图可见的那一版</text>
</svg>
上半是回滚：每种修改都留了一条能反着做的记录。下半是 MVCC：当前行用回滚指针指向 undo 里的旧版本，旧版本再指向更旧的，连成链。
**举个例子。** 账户行 `(id=1, 余额=100)`：
1. **事务 A 更新：** 余额改成 50。undo 里记下「余额旧值 100」，行上的回滚指针指向这条 undo。
2. **事务 A 回滚：** 读 undo，把余额写回 100，更新被撤销。
3. **事务 B 在 A 提交前做快照读：** 当前版本余额 50 来自还没提交的 A，B 看不到；顺着指针找到 undo 里的 100，B 读到 100。
4. **A 提交后：** update undo 还要留着，因为 B 的读视图可能还要用；直到没有读视图需要，purge 才清理。
5. **长事务例子：** B 一直不结束，期间这一行又被更新 2 万次，undo 链上堆了 2 万个版本，`History list length` 约 2 万。
**容易错。**
- **以为 undo 记的是整行快照：** 更新只记被改列的旧值，插入和删除都只记主键等少量信息，不是每次都存整行。
- **以为提交后 undo 马上删：** 只有 insert undo 可以；update undo 要等读视图都不需要才清理。
- **以为回滚比正向执行快：** 回滚要把每一步反着做一遍，大事务回滚往往比正向执行还慢，期间锁一直占着。
- **忽略长事务：** 一个忘记提交的读事务就能拖住整个 undo 清理。
**业务场景。** 批量发券事务更新 10 万行，第 8 万行因唯一键冲突失败要整体回滚：undo 逐行恢复 8 万行，比正向执行还慢，期间锁一直占着；批量操作应拆成每批几百到几千行的小事务。

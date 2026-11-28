---
id: bagu-sql-handwrite-1-group-join-window
node: b.mysql.sql-handwrite
type: qa
step: 1
---
## Q
**SQL 手撕 · 分组、连接与窗口函数**｜必会

面试官：「成绩表（姓名、课程、分数），查出所有选修课程分数都大于 80 的学生；再写一个每门课取前 N 名的查询。」

## A
**基本回答。** 「全部成立」转成「最小值也成立」：`GROUP BY name HAVING MIN(score) > 80`，或 `NOT EXISTS` 找不到分数不超过 80 的记录。每组取前 N：`ROW_NUMBER() OVER (PARTITION BY course ORDER BY score DESC)` 编号，窗口函数不能直接放 `WHERE`，所以包一层子查询，外层取 `rn <= N`（需要 MySQL 8.0）。`WHERE` 在分组前过滤行，聚合条件只能放 `HAVING`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同一门课按分数倒序，出现两个 90 分</text>
<rect x="10" y="24" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="35" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">姓名</text>
<rect x="60" y="24" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分数</text>
<rect x="110" y="24" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">row_number</text>
<rect x="190" y="24" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">rank</text>
<rect x="250" y="24" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dense_rank</text>
<rect x="10" y="50" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="35" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">甲</text>
<rect x="60" y="50" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">95</text>
<rect x="110" y="50" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="190" y="50" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="250" y="50" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="10" y="76" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="35" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">乙</text>
<rect x="60" y="76" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">90</text>
<rect x="110" y="76" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="190" y="76" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="250" y="76" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="10" y="102" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="35" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">丙</text>
<rect x="60" y="102" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">90</text>
<rect x="110" y="102" width="80" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="190" y="102" width="60" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="220" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="250" y="102" width="80" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="290" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="10" y="128" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="35" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">丁</text>
<rect x="60" y="128" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">85</text>
<rect x="110" y="128" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="190" y="128" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="250" y="128" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="10" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">丙与乙并列：rank 都是 2，下一名跳到 4</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">dense_rank 不跳号，下一名是 3</text>
<text x="10" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">row_number 不并列，硬排成 2、3</text>
<text x="10" y="232" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">取每组前 N：外层再 WHERE rn &lt;= N</text>
</svg>
同一门课甲 95、乙 90、丙 90、丁 85：看丙那一行，`ROW_NUMBER` 不并列得 3，`RANK` 并列得 2 且下一名跳到 4，`DENSE_RANK` 并列得 2 且下一名是 3。要保留并列的人就用后两个。
**NULL 陷阱。** `MIN` 忽略 NULL，有一门成绩为空的人也会通过；排除要写 `HAVING SUM(score <= 80 OR score IS NULL) = 0`，或在 `NOT EXISTS` 里加 `OR score IS NULL`。`NOT IN` 的子查询含 NULL 时整个条件永远不成立、查不出任何行，所以优先 `NOT EXISTS`。
**举个例子。** 张三 数学 90、英语 85；李四 数学 95、英语 NULL；王五 数学 70、英语 99。`HAVING MIN(score) > 80` 通过张三和李四，李四英语为空却被判通过；改成 `SUM(...) = 0` 后只剩张三。每科前 2 名：数学 95、90、70 编号 1、2、3，取 `rn <= 2` 得李四和张三。
**容易错。**
- **以为 MIN 会处理 NULL：** 成绩为空的人会误通过。
- **用 NOT IN：** 子查询含 NULL 结果为空。
- **聚合条件写进 WHERE：** 分组前还没有聚合值。

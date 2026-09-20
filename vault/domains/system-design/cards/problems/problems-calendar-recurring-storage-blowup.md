---
id: problems-calendar-recurring-storage-blowup
node: problems.realtime.calendar
type: qa
step: 3
tags: [grown]
---
## Q
For a calendar design where 6 million recurring event series are created per day and a typical daily-recurring series runs for about 2 years (730 occurrences) before ending, compare the annual storage cost of storing one rule row per series versus materializing every future occurrence as its own row (both at about 300 bytes/row). What is the storage ratio, and why is a series with no COUNT or UNTIL an even stronger case for the rule-based approach?

## A
Rule-based storage: 6,000,000 × 365 = 2.19×10^9 rows/year ≈ 0.657 TB/year. Materialized instances: 2.19×10^9 × 730 ≈ 1.5987×10^12 rows/year ≈ 479.61 TB/year — about 730x more storage. A series with no COUNT or UNTIL (repeats forever) makes this even stronger: materializing it would require an unbounded number of rows, while expanding the rule on demand for a query window still only produces at most as many instances as the window can contain, regardless of how long the series has existed.

## Q zh
在一个日历设计里，每天新创建 600 万个循环事件系列，一个典型的每日循环系列在结束前平均持续约 2 年（730 次发生）。比较「每个系列只存一条规则行」和「把每一次未来发生都物化成一行」这两种方式的年度存储成本（都按约 300 字节/行计算）。存储比例是多少？为什么一个没有 COUNT 或 UNTIL 的系列会让「存规则」这个方案的优势更明显？

## A zh
按规则存储：6,000,000 × 365 = 2.19×10^9 行/年 ≈ 0.657 TB/年。按实例物化：2.19×10^9 × 730 ≈ 1.5987×10^12 行/年 ≈ 479.61 TB/年——约多出 730 倍存储。一个没有 COUNT 或 UNTIL（永远重复）的系列会让这个优势更明显：物化它需要无限多行，而按需为查询窗口展开规则，无论这个系列已经存在了多久，产生的实例数量最多只取决于查询窗口本身能容纳多少个。

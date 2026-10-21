---
id: amz-in-memory-db-limit-before-order-mistake
node: amazon.amz-in-memory-db
type: qa
step: 9
tags: [grown]
---
## Q
在内存数据库的 select 里，先 LIMIT 再 ORDER BY 会出什么错？给一个具体输入，并说明修复。

## A
三行工资依次是 5、30、10，要「按工资降序取第 1 行」。先 LIMIT 1 得到 `[5]`，再排序还是 5；正确答案是 30。

修复：严格按逻辑顺序处理：FROM → JOIN → WHERE → ORDER BY → LIMIT → 投影。WHERE 也要在 JOIN 之后，否则引用右表列的条件找不到列。`select` 写成一个直线函数，这个顺序本身就是文档。

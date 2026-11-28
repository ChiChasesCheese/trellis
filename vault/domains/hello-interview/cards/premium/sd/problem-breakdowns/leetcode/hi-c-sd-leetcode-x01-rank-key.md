---
id: hi-c-sd-leetcode-x01-rank-key
node: sd.problem-breakdowns.leetcode.exam
type: qa
step: 11
---
## Q
**在线判题平台 · 排名口径与有序集合分数**｜考点 · 必会

排行榜规则：解出题数多者在前，并列时"最后一道题的解出时间"早者在前。有人这样写聚合：`SELECT userId, COUNT(DISTINCT problemId), MIN(submittedAt) ... WHERE passed GROUP BY userId`。（1）错在哪里？（2）搬进 Redis 有序集合只有一个数值分数，怎么编码？

## A
- **错误一，时间口径：** `MIN(submittedAt)` 取的是该用户最早一次通过，不是最后解出那道题的时间。同一题多次通过的重复提交也会混进来。应先按（用户，题目）取首次通过时间，再按用户取最大值：

```sql
SELECT userId, COUNT(*) AS solved, MAX(firstPass) AS lastSolve
FROM (SELECT userId, problemId, MIN(submittedAt) AS firstPass
      FROM submissions WHERE competitionId = :c AND passed
      GROUP BY userId, problemId) t
GROUP BY userId ORDER BY solved DESC, lastSolve ASC
```

- **编码：** 时间用相对比赛开始的秒数。把两个排序键压进一个数：`score = solved × 10000 − lastSolveSeconds`。比赛 90 分钟 = 5400 秒，远小于 10000，所以先比解题数，再比时间，且时间越小分越高。例：8 题、4000 秒得 76000；8 题、3500 秒得 76500，排前；9 题、5400 秒得 84600，排最前。用 `ZRANGE ... REV` 取前几名。
- **边界：** 分数是双精度浮点数，在 2^53 以内整数精确，这里远不到；分数完全相同时，Redis 按成员字典序排序，需要稳定名次时可再把 userId 次序纳入口径。

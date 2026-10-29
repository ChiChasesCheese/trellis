---
id: uth-gaps-dp-join-order-4-collapse-limit
node: gaps.dp-join-order
type: qa
step: 4
---
## Q
**写在 SQL 里的 JOIN 顺序，规划器听吗**｜PostgreSQL · 17

`FROM a JOIN b ON … JOIN c ON … JOIN d …` 写了很多个显式 JOIN，PostgreSQL 会重新安排顺序吗？最多重排多少张表？

## A
**结构。** 会：规划器先把显式 `JOIN` 摊平成一个 FROM 列表，再对整个列表做逐层 DP。

**细节。**

- `join_collapse_limit` 默认 8：摊平后不超过 8 项才摊平；子查询并入上层用 `from_collapse_limit`，默认也是 8
- 超过限制的部分保持你写的结构，只在每一块里面重排
- 设为 1：完全不重排，SQL 里写的顺序就是实际连接顺序
- 全外连接（FULL JOIN）不参与摊平

**为什么。** DP 的运行时间随列表项数指数增长，限制列表长度就是限制规划时间；代价是超过限制时可能错过更好的顺序。

**坑。** 规划器估错行数、选了很差的顺序时，高级用户可以临时把 `join_collapse_limit` 设为 1，自己写定顺序。

**对应 LeetCode：** 无直接对应的题

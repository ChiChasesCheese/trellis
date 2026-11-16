---
id: lcp-issue-creation-api-reflection-optimistic-vs-row-lock
node: lcproject.lcp-issue-creation-api
type: qa
step: 5
tags: [作答]
---
## Q
两个同事同时打开同一张工单的页面，各自读到版本 1，再各自发请求改状态。工单服务把数据放进数据库后，比较"乐观版本检查"和"数据库行锁"：各自怎么工作、什么时候选哪个、代价是什么？

## A
**评分点**
- 说出乐观检查的机制：版本放在行里，`UPDATE ... WHERE id=? AND version=?` 受影响行数为 0 就是冲突，回 409 让客户端重新读
- 说出乐观检查不持有锁跨请求：读与写是两个 HTTP 请求，冲突少时几乎没有成本
- 说出乐观检查的代价：冲突多时客户端不停重试，热点行会被饿死
- 说出行锁（`SELECT ... FOR UPDATE`）在一个事务里先锁再改，别人排队；它保护事务内部的读改写
- 说出行锁的代价：锁不能在用户思考的时间里跨请求持有，长事务拖住别人并可能死锁
- 说出两者常配合：版本字段管跨请求的"你读到的还是最新吗"，单条带条件的 UPDATE 或行锁管单次写入的原子性

<details class="pt"><summary>参考答案</summary>

乐观检查把版本放在行里：`UPDATE issues SET status=?, version=version+1 WHERE id=? AND version=?`，受影响行数为 0 就回 409。不跨请求持锁，冲突少时几乎没成本，冲突多了客户端反复重试、热点行会饿死。行锁在一个事务里先锁再改，别人排队，保护的是事务内部的读改写，但 GET 与 PATCH 是两个请求，锁没法在用户思考时一直持有，长事务还会引发死锁。常见做法是两者并用。

</details>

**知识点：** 复合操作（Compound Actions）、重试与退避（Retry & Backoff）、线程安全结构的写法（Thread-Safe Structures）

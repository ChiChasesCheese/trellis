---
id: lcp-actor-follow-notifications-contract-rules
node: lcproject.lcp-actor-follow-notifications
type: qa
step: 1
tags: [作答]
---
## Q
CastWatch 的用户可以关注演员；登记一部新片（`add_movie(movie_id, title, actors)`）时，要给关注了卡司的人发通知，`inbox(user)` 读取通知。现有服务的症状是：通知丢失、取关无效、重试导入行为混乱、收件箱顺序不对，多个线程会同时调用。开工前你会先定下哪几条规则？

## A
**评分点**
- 说出受众是"关注了卡司中任意一人"的用户，每人恰好一条：关注多个卡司成员、卡司里有重复 id 都只一条；空卡司不通知任何人
- 说出重复导入（同 id、同片名、卡司集合相等）返回 False 且不产生通知，哪怕关注者变了；卡司按集合比较，顺序和重复无关
- 说出同 id 但片名或卡司集合不同抛 RuntimeError("movie_conflict")，并且什么状态都不改
- 说出收件箱按电影成功登记的先后返回，不是按 id 排序；返回独立副本，取关不删历史，关注不回填
- 说出校验先于一切：非法输入抛 ValueError("invalid_input")，发生在改状态之前，也先于冲突检查
- 说出并发调用等价于某个串行顺序，不能留半截状态

<details class="pt"><summary>参考答案</summary>

先把合同写成六条：受众是卡司任一成员的关注者并集，每人一条；相同的重复导入返回 `False` 且无通知；同 id 内容不同抛 `movie_conflict` 且不改状态；收件箱按登记顺序、返回副本，取关不删历史、关注不回填；校验在改状态之前、先于冲突；并发等价于某个串行顺序。每条配一个带具体数据的测试，再让智能体动手。

</details>

**知识点：** 边界校验（Validate at the Boundary）、复合操作（Compound Actions）、防御性拷贝（Defensive Copying）
